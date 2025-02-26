from django.db import models



class Driver(models.Model):
    full_name = models.CharField(max_length=255)
    car_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="drivers_photo/", null=True, blank=True)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)
    telegram_id = models.CharField(max_length=50, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField()

    def __str__(self):
        return self.full_name
    