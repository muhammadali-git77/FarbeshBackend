"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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