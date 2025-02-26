# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreateSerializer, OrderSerializer
from rest_framework import permissions
import requests
from rest_framework_simplejwt.tokens import RefreshToken



#ORDER
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

            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": TELEGRAM_GROUP_ID, "text": text}

            try:
                response = requests.post(url, data=payload)
                telegram_response = response.json()

                if telegram_response.get("ok"):
                    return Response({"message": "Buyurtma qabul qilindi!"}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "Telegramga jo‘natishda xatolik!", "details": telegram_response},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except Exception as e:
                return Response(
                    {"error": "Xatolik yuz berdi!", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
