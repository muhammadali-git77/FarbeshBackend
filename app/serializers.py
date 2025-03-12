from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import permissions




User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Parolni faqat yozish uchun

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


#ORDER
class OrderSerializer(serializers.Serializer):
    DIRECTION_CHOICES = [
        ("Farg'ona-Beshariq", "Farg'ona-Beshariq"),
        ("Beshariq-Farg'ona", "Beshariq-Farg'ona"),
    ]

    GENDER_CHOICES = [
        ("male", "Erkak"),
        ("female", "Ayol"),
        ("mail", "Pochta")
    ]

    direction = serializers.ChoiceField(choices=DIRECTION_CHOICES)
    phone_number = serializers.CharField(max_length=13)
    passengers_count = serializers.IntegerField(min_value=0)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    latitude = serializers.FloatField(required=True, allow_null=True)  # Lokatsiya koordinatalari
    longitude = serializers.FloatField(required=True,allow_null=True)

  