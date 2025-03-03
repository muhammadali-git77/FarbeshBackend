
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view, api_v1_view, api_v2_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),

    path("api/v1/", include("app.urls")),
    path("api/v1/home/", api_v1_view, name="api-v1-home"),

    path("api/v2/", include("drivers_admin.urls")),
    path("api/v2/home/", api_v2_view, name="api-v2-home"),

    # Authentifikatsiya va ro‘yxatdan o‘tish
    path("api/auth/", include("dj_rest_auth.urls")),  # Login, logout, user info
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),  # Registratsiya

    # JWT Token uchun URL'lar
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login (token olish)
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Token yangilash
    path("api/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),  # Tokenni tekshirish
]






if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
