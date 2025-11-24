from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
User = get_user_model()


class Restaurant(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=200,verbose_name="nom")
    description = models.TextField(blank=True,verbose_name="description")
    image = models.ImageField(upload_to='restaurants/', blank=True)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    # Horaires (format JSON pour flexibilité)
    opening_hours = models.JSONField(default=dict)

    # Statut et ratings
    is_active = models.BooleanField(default=True)
    is_accepting_orders = models.BooleanField(default=True)
    average_rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)

    # Livraison
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    free_delivery_threshold = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    delivery_radius_km = models.FloatField(default=5.0)
    estimated_delivery_time = models.IntegerField(default=30, help_text="En minutes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True)

    # Disponibilité
    is_available = models.BooleanField(default=True, verbose_name="est disponible")
    preparation_time = models.IntegerField(default=15, help_text="En minutes")

    # Options et personnalisations
    has_options = models.BooleanField(default=False)
    options = models.JSONField(default=dict, blank=True, help_text="Options et suppléments")

    # Nutrition et allergènes
    calories = models.IntegerField(null=True, blank=True)
    allergens = models.JSONField(default=list, blank=True)

    # Stats
    order_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_count', 'name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.name}"


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['restaurant', 'customer']
        ordering = ['-created_at']