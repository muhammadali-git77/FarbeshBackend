from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework import permissions
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

TELEGRAM_BOT_TOKEN = '7800984825:AAEPAd2o_vtfrGlUwc7X7g2wHPCbJmriaX8'
TELEGRAM_GROUP_ID = "-1002446857055"

order_owners = {}  # Buyurtmani kim bosganini saqlash uchun


class SendOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            gender_text = "Erkak" if data["gender"] == "male" else "Ayol" if data["gender"] == "female" else "Po'chta"


            if data["gender"] == "mail":
                text = (
                    f"🚖 **Yangi Buyurtma** 🚖\n"
                    f"📍 Yo‘nalish: {data['direction']}\n"
                    f"📞 Telefon: {data['phone_number']}\n"
                    f"📦 Pochta: ✅"
            )
            else:
                text = (
                    f"🚖 **Yangi Buyurtma** 🚖\n"
                    f"📍 Yo‘nalish: {data['direction']}\n"
                    f"📞 Telefon: {data['phone_number']}\n"
                    f"👥 Yo‘lovchilar: {data['passengers_count']} ({gender_text})"
                )

            buttons = {
                "inline_keyboard": [
                    [{"text": "Buyurtmani olish", "callback_data": "confirm"}]
                ]
            }

            message_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            location_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendLocation"

            try:
                message_payload = {
                    "chat_id": TELEGRAM_GROUP_ID,
                    "text": text,
                    "reply_markup": json.dumps(buttons)
                }

                if "latitude" in data and "longitude" in data:
                    location_payload = {
                        "chat_id": TELEGRAM_GROUP_ID,
                        "latitude": float(data["latitude"]),
                        "longitude": float(data["longitude"])
                    }
                    location_response = requests.post(location_url, data=location_payload).json()
                    if location_response.get("ok"):
                        message_payload["reply_to_message_id"] = location_response["result"]["message_id"]

                message_response = requests.post(message_url, data=message_payload).json()

                if message_response.get("ok"):
                    order_owners[message_response["result"]["message_id"]] = None

                if not message_response.get("ok"):
                    return Response({"error": "Telegramga jo‘natishda xatolik!", "details": message_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({"message": "Buyurtma qabul qilindi!"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": "Xatolik yuz berdi!", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            update = request.data
            if "callback_query" in update:
                callback = update["callback_query"]
                callback_data = callback["data"]
                chat_id = callback["message"]["chat"]["id"]
                message_id = callback["message"]["message_id"]
                user_name = callback["from"]["first_name"]
                user_id = callback["from"]["id"]

                owner_id = order_owners.get(message_id)

                if callback_data == "confirm":
                    if owner_id is None:
                        order_owners[message_id] = user_id
                        new_buttons = {
                            "inline_keyboard": [
                                [{"text": "✅ Buyurtma olindi", "callback_data": "done"}],
                                [{"text": "❌ Bekor qilish", "callback_data": f"cancel:{user_id}"}]
                            ]
                        }
                    elif owner_id == user_id:
                        new_buttons = {
                            "inline_keyboard": [
                                [{"text": "✅ Buyurtma olindi", "callback_data": "done"}],
                                [{"text": "❌ Bekor qilish", "callback_data": f"cancel:{user_id}"}]
                            ]
                        }
                    else:
                        new_buttons = {
                            "inline_keyboard": [
                                [{"text": "✅ Buyurtma olindi", "callback_data": "done"}]
                            ]
                        }
                elif callback_data.startswith("cancel") and str(user_id) == callback_data.split(":")[1]:
                    new_buttons = {"inline_keyboard": [
                        [{"text": "Buyurtmani olish", "callback_data": "confirm"}]
                    ]}
                    order_owners[message_id] = None
                else:
                    return Response({"message": "Siz bu amalni bajara olmaysiz"}, status=status.HTTP_403_FORBIDDEN)

                edit_payload = {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "reply_markup": json.dumps(new_buttons)
                }
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageReplyMarkup", data=edit_payload)
                return Response({"message": "Callback qabul qilindi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Xatolik yuz berdi!", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Hech qanday amal bajarilmadi"}, status=status.HTTP_200_OK)
