
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, api_v1_view, api_v2_view

urlpatterns = [
    path("", home_view, name="home"),  # Barcha URL'larni chiqarish
    path("admin/", admin.site.urls),

    path("api/v1/", include("app.urls")),  # Oddiy foydalanuvchilar API
    path("api/v1/home/", api_v1_view, name="api-v1-home"),  # api/v1 uchun barcha URL'larni chiqarish

    path("api/v2/", include("drivers_admin.urls")),  # Admin API
    path("api/v2/home/", api_v2_view, name="api-v2-home"),  # api/v2 uchun barcha URL'larni chiqarish

    path("api/auth/", include("dj_rest_auth.urls")),  # Auth tizimi
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),  # Registratsiya
    # path("api/allauth/", include("allauth.urls")),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)