from django.urls import reverse
from django.http import JsonResponse

BASE_URL = "https://farbesh.up.railway.app"

def home_view(request):
    """ Barcha mavjud URL'larni chiqaruvchi asosiy sahifa """
    urls = {
        # "Admin Panel": f"{BASE_URL}{reverse('admin:index')}",
        "Foydalanuvchilar API": f"{BASE_URL}/api/v1/",
        "Admin API": f"{BASE_URL}/api/v2/",
        "Login": f"{BASE_URL}/auth/login/",
        "Logout": f"{BASE_URL}/auth/logout/",
        "Profile": f"{BASE_URL}/auth/user/",
        "Parolni o'zgartirish": f"{BASE_URL}/auth/password/change/",
        "Registratsiya": f"{BASE_URL}/auth/registration/",
        # "AllAuth API": f"{BASE_URL}/api/allauth/",
    }
    return JsonResponse(urls)


def api_v1_view(request):
    """ api/v1/ uchun yo‘llarni JSON formatida chiqarish """
    urls = {
        "Foydalanuvchilar API Asosiy": f"{BASE_URL}/api/v1/",
        "Buyurtma Yuborish": f"{BASE_URL}/api/v1/",
    }
    return JsonResponse(urls)


def api_v2_view(request):
    """ api/v2/ (Admin API) uchun yo‘llarni JSON formatida chiqarish """
    urls = {
        "Admin API Asosiy": f"{BASE_URL}/api/v2/",
        "Haydovchilar Ro‘yxati": f"{BASE_URL}/api/v2/drivers/",
        "Haydovchi Tafsilotlari": f"{BASE_URL}/api/v2/drivers/<int:pk>/",
    }
    return JsonResponse(urls)
