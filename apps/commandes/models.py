from django.db import models
from apps.restaurants.models import Restaurant,MenuItem
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('preparing', 'En préparation'),
        ('ready', 'Prête'),
        ('picked_up', 'Récupérée'),
        ('delivered', 'Livrée'),
        ('cancelled', 'Annulée'),
    )

    PAYMENT_METHODS = (
        ('cash', 'Espèces'),
        ('card', 'Carte'),
        ('mobile', 'Paiement mobile'),
    )

    # Identifiants
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True)

    # Relations
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')

    # Statut et timing
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)

    # Prix
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Paiement
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, default='pending')

    # Adresse de livraison
    delivery_address = models.JSONField()
    delivery_latitude = models.FloatField()
    delivery_longitude = models.FloatField()

    # Notes
    customer_notes = models.TextField(blank=True)
    restaurant_notes = models.TextField(blank=True)
    driver_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Commande #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Génère un numéro de commande unique
            import random
            import string
            self.order_number = ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    # Options sélectionnées (JSON)
    selected_options = models.JSONField(default=dict, blank=True)
    special_instructions = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity}"