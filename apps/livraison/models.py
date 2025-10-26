from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
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


class DriverRating(models.Model):
    """Évaluation d'un livreur par un client"""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='driver_rating')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings_received')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_ratings_given')

    # Notes (sur 5)
    overall_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Note globale"
    )
    punctuality_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Ponctualité",
        null=True,
        blank=True
    )
    professionalism_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Professionnalisme",
        null=True,
        blank=True
    )
    care_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Soin de la commande",
        null=True,
        blank=True
    )

    # Commentaire
    comment = models.TextField(blank=True, verbose_name="Commentaire")

    # Pourboire
    tip_amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name="Pourboire"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Évaluation de livreur"
        verbose_name_plural = "Évaluations de livreurs"

    def __str__(self):
        return f"Rating {self.overall_rating}/5 pour {self.driver.username} par {self.customer.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mettre à jour la moyenne du livreur
        self.update_driver_average()

    def update_driver_average(self):
        """Met à jour la moyenne de notation du livreur"""
        from django.db.models import Avg
        ratings = DriverRating.objects.filter(driver=self.driver)
        average = ratings.aggregate(Avg('overall_rating'))['overall_rating__avg']

        # Mettre à jour le profil du livreur
        if hasattr(self.driver, 'driver_profile'):
            self.driver.driver_profile.average_rating = average or 0.0
            self.driver.driver_profile.total_ratings = ratings.count()
            self.driver.driver_profile.save()