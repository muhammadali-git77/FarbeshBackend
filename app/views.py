from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework import permissions
import requests
import json
from django.urls import path

# ORDER
TELEGRAM_BOT_TOKEN = "7795180366:AAFlB0h52Mf-wkK61ESb6b6__n1c6_pbNgw"
TELEGRAM_GROUP_ID = "-1002446857055"

class SendOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            gender_text = "Erkak" if data["gender"] == "male" else "Ayol"

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
                if "latitude" in data and "longitude" in data:
                    location_payload = {
                        "chat_id": TELEGRAM_GROUP_ID,
                        "latitude": data["latitude"],
                        "longitude": data["longitude"]
                    }
                    location_response = requests.post(location_url, data=location_payload).json()
                    if location_response.get("ok"):
                        message_payload = {
                            "chat_id": TELEGRAM_GROUP_ID,
                            "text": text,
                            "reply_to_message_id": location_response["result"]["message_id"],
                            "reply_markup": json.dumps(buttons)
                        }
                else:
                    message_payload = {
                        "chat_id": TELEGRAM_GROUP_ID,
                        "text": text,
                        "reply_markup": json.dumps(buttons)
                    }

                message_response = requests.post(message_url, data=message_payload).json()
                if not message_response.get("ok"):
                    return Response(
                        {"error": "Telegramga jo‘natishda xatolik!", "details": message_response},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                return Response({"message": "Buyurtma qabul qilindi!"}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response(
                    {"error": "Xatolik yuz berdi!", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class TelegramCallbackView(APIView):
    def post(self, request):
        try:
            update = request.data

            if "callback_query" in update:
                callback = update["callback_query"]
                callback_data = callback["data"]
                chat_id = callback["message"]["chat"]["id"]
                message_id = callback["message"]["message_id"]
                user_name = callback["from"]["first_name"]

                if callback_data == "confirm":
                    new_buttons = {
                        "inline_keyboard": [
                            [{"text": "Bekor qilish", "callback_data": "cancel"}]
                        ]
                    }
                    edit_payload = {
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "reply_markup": json.dumps(new_buttons)
                    }
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageReplyMarkup", data=edit_payload)

                    text = f"✅ Buyurtma olindi: {user_name}"
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data={
                        "chat_id": chat_id,
                        "text": text,
                        "reply_to_message_id": message_id
                    })

                elif callback_data == "cancel":
                    new_buttons = {
                        "inline_keyboard": [
                            [{"text": "Buyurtmani olish", "callback_data": "confirm"}]
                        ]
                    }
                    edit_payload = {
                        "chat_id": chat_id,
                        "message_id": message_id,
                        "reply_markup": json.dumps(new_buttons)
                    }
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageReplyMarkup", data=edit_payload)

                    text = f"🚫 Buyurtma bekor qilindi: {user_name}"
                    requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data={
                        "chat_id": chat_id,
                        "text": text,
                        "reply_to_message_id": message_id
                    })

            return Response({"message": "Callback qabul qilindi"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Xatolik yuz berdi!", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
