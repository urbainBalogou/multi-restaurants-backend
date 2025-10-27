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

    DRIVER_STATUS = (
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('suspended', 'Suspendu'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')

    # Restaurant qui gère ce livreur (si null, c'est un livreur indépendant)
    managed_by_restaurant = models.ForeignKey(
        'restaurants.Restaurant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_drivers',
        verbose_name="Géré par le restaurant"
    )

    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    license_plate = models.CharField(max_length=20)

    # Statut du livreur
    status = models.CharField(max_length=20, choices=DRIVER_STATUS, default='pending')
    is_available = models.BooleanField(default=False, verbose_name="Disponible")

    # Localisation
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    # Documents
    driver_license_number = models.CharField(max_length=50, blank=True, verbose_name="Numéro de permis")
    driver_license_photo = models.ImageField(upload_to='drivers/licenses/', blank=True)
    id_card_photo = models.ImageField(upload_to='drivers/ids/', blank=True)
    vehicle_insurance = models.ImageField(upload_to='drivers/insurance/', blank=True)

    # Ratings
    average_rating = models.FloatField(default=0.0, verbose_name="Note moyenne")
    total_ratings = models.IntegerField(default=0, verbose_name="Nombre d'évaluations")
    total_deliveries = models.IntegerField(default=0, verbose_name="Nombre de livraisons")

    # Revenus
    total_tips = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total pourboires")
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total des revenus")

    # Préférences de livraison
    max_delivery_distance_km = models.FloatField(default=10.0, verbose_name="Distance max (km)")
    preferred_zones = models.JSONField(default=list, blank=True, help_text="Zones préférées")

    # Horaires de disponibilité
    availability_schedule = models.JSONField(
        default=dict,
        blank=True,
        help_text="Horaires de disponibilité par jour"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_vehicle_type_display()}"

    @property
    def is_independent(self):
        """Vérifie si le livreur est indépendant"""
        return self.managed_by_restaurant is None




