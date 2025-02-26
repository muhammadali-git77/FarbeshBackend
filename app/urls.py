from django.urls import path
from .views import SendOrderView



urlpatterns = [
    path("send_order/", SendOrderView.as_view(), name="send_order"),
]
