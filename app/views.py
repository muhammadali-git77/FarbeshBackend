from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework import permissions
import requests
import json
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
            message_payload = {
                "chat_id": TELEGRAM_GROUP_ID,
                "text": text,
                "reply_markup": json.dumps(buttons)
            }
            message_response = requests.post(message_url, data=message_payload).json()

            if message_response.get("ok"):
                return Response({"message": "Buyurtma qabul qilindi!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Telegramga jo‘natishda xatolik!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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

                if callback_data == "confirm":
                    new_buttons = {
                        "inline_keyboard": [
                            [{"text": "✅ Buyurtma olindi", "callback_data": "confirmed", "callback_data": f"confirmed:{user_id}"}],
                            [{"text": "Bekor qilish", "callback_data": f"cancel:{user_id}"}]
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

                elif callback_data.startswith("cancel"):
                    _, owner_id = callback_data.split(":")
                    if str(user_id) == owner_id:
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
            return Response({"error": "Xatolik yuz berdi!", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
