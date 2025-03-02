from django.urls import path
from .views import SendOrderView, TelegramCallbackView




urlpatterns = [
    path("send_order/", SendOrderView.as_view(), name="send_order"),
    path("telegram/callback/", TelegramCallbackView.as_view(), name="telegram_callback"),
]

