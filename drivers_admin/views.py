from django.shortcuts import render
from rest_framework import status, generics
from rest_framework import permissions
from .models import Driver
from .serializers import DriverSerializer, AdminProfileSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters



class DriverListCreateView(generics.ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAdminUser]  
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]  
    filterset_fields = ['payment_status', 'joined_at']
    search_fields = ['full_name', 'car_name', 'phone_number', 'telegram_id']



class DriverRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAdminUser]



from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated  # Faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun
from django.contrib.auth.models import User
from .serializers import AdminProfileSerializer  # Serializerni import qilish
from rest_framework import serializers

class AdminProfileView(RetrieveUpdateAPIView):
    """
    Admin o'zi haqidagi ma'lumotlarni ko'rish va yangilash uchun View.
    """
    serializer_class = AdminProfileSerializer  # Serializerni biriktirish
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyadan o'tgan foydalanuvchilar uchun

    def get_object(self):
        """
        Joriy foydalanuvchi obyektini qaytarish.
        """
        user = self.request.user
        if user is None or user.is_anonymous:
            raise serializers.ValidationError("Foydalanuvchi autentifikatsiyadan o'tmagan.")
        return user