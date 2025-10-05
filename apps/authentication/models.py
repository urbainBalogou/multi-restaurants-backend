from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Client'),
        ('restaurant', 'Restaurant'),
        ('driver', 'Livreur'),
        ('admin', 'Administrateur'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone_number = PhoneNumberField(blank=True)
    address = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class CustomerProfile(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE, related_name='customer_profile')
    delivery_addresses = models.JSONField(default=list, blank=True)
    favorite_restaurants = models.ManyToManyField('restaurants.Restaurant', blank=True)


class DriverProfile(models.Model):
    VEHICLE_TYPES = (
        ('bike', 'Vélo'),
        ('scooter', 'Scooter'),
        ('car', 'Voiture'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    license_plate = models.CharField(max_length=20)
    is_available = models.BooleanField(default=False)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)




