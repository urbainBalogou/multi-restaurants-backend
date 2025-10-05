from django.db import models
from django.contrib.auth import get_user_model
from apps.commandes.models import Order

User = get_user_model()


class DeliveryTracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='tracking')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracking_deliveries')

    # Position actuelle du livreur
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)

    # Temps estimé
    estimated_arrival = models.DateTimeField(null=True, blank=True)
    distance_remaining_km = models.FloatField(null=True, blank=True)

    # Statuts de livraison
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DeliveryZone(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='delivery_zones')

    # Zone géographique (polygon)
    coordinates = models.JSONField(help_text="Coordonnées du polygone de la zone")
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_time = models.IntegerField(help_text="Temps estimé en minutes")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"