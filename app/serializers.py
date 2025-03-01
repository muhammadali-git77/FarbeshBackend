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
    ]

    direction = serializers.ChoiceField(choices=DIRECTION_CHOICES)
    location = serializers.JSONField()  # Lokatsiya uchun JSON field
    phone_number = serializers.CharField(max_length=13)
    passengers_count = serializers.IntegerField(min_value=1)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)

    def validate_location(self, value):
        if not isinstance(value, dict) or 'latitude' not in value or 'longitude' not in value:
            raise serializers.ValidationError("Location must contain 'latitude' and 'longitude' fields.")
        return value