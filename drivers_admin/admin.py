from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'car_name', 'age', 'phone_number', 'telegram_id', 'joined_at', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'joined_at')
    search_fields = ('full_name', 'car_name', 'phone_number', 'telegram_id')
    ordering = ('-joined_at',)
