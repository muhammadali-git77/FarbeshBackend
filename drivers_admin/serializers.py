from rest_framework import serializers
from .models import Driver
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.contrib.auth.password_validation import validate_password



class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'




from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class AdminProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,  # Parolni faqat yozish uchun
        required=False,   # Parolni yangilash ixtiyoriy
        validators=[validate_password]  # Parolni validatsiya qilish
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Kerakli maydonlar

    def update(self, instance, validated_data):
        # Ma'lumotlarni yangilash
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        # Parolni yangilash (agar kiritilgan bo'lsa)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)  # Parolni xavfsiz tarzda yangilash

        instance.save()
        return instance