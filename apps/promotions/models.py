from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from decimal import Decimal

User = get_user_model()


class Coupon(models.Model):
    """Code promo utilisable par les clients"""

    DISCOUNT_TYPES = (
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
        ('free_delivery', 'Livraison gratuite'),
    )

    code = models.CharField(max_length=50, unique=True, verbose_name="Code promo")
    description = models.TextField(blank=True)

    # Type de réduction
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Pourcentage (0-100) ou montant fixe"
    )

    # Conditions d'utilisation
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Montant minimum de commande"
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Montant maximum de réduction (pour les pourcentages)"
    )

    # Validité
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Limitations
    usage_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="Nombre total d'utilisations autorisées"
    )
    usage_limit_per_user = models.IntegerField(
        default=1,
        help_text="Nombre d'utilisations par utilisateur"
    )
    usage_count = models.IntegerField(default=0)

    # Restaurants applicables (si vide, applicable à tous)
    applicable_restaurants = models.ManyToManyField(
        Restaurant,
        blank=True,
        related_name='coupons'
    )

    # Utilisateurs autorisés (si vide, tous les utilisateurs)
    allowed_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='exclusive_coupons'
    )

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}"

    def is_valid(self):
        """Vérifie si le coupon est valide"""
        from django.utils import timezone
        now = timezone.now()

        if not self.is_active:
            return False, "Le coupon n'est pas actif"

        if now < self.valid_from:
            return False, "Le coupon n'est pas encore valide"

        if now > self.valid_until:
            return False, "Le coupon a expiré"

        if self.usage_limit and self.usage_count >= self.usage_limit:
            return False, "Le coupon a atteint sa limite d'utilisation"

        return True, "Coupon valide"

    def calculate_discount(self, order_amount):
        """Calcule le montant de la réduction"""
        if self.discount_type == 'percentage':
            discount = order_amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        elif self.discount_type == 'fixed':
            discount = self.discount_value
        else:  # free_delivery
            discount = Decimal('0.00')  # La livraison sera gratuite

        return min(discount, order_amount)  # Ne peut pas dépasser le montant de la commande


class CouponUsage(models.Model):
    """Historique d'utilisation des coupons"""

    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_usages')
    order = models.ForeignKey('commandes.Order', on_delete=models.CASCADE, related_name='coupon_usage')

    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-used_at']
        verbose_name = "Utilisation de coupon"
        verbose_name_plural = "Utilisations de coupons"

    def __str__(self):
        return f"{self.coupon.code} - {self.user.username} - {self.used_at}"


class Promotion(models.Model):
    """Promotions des restaurants (réductions temporaires sur articles)"""

    PROMOTION_TYPES = (
        ('percentage', 'Pourcentage'),
        ('fixed', 'Montant fixe'),
        ('buy_x_get_y', 'Achetez X obtenez Y'),
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='promotions')
    name = models.CharField(max_length=200, verbose_name="Nom de la promotion")
    description = models.TextField(blank=True)

    # Type de promotion
    promotion_type = models.CharField(max_length=20, choices=PROMOTION_TYPES)
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Pourcentage ou montant fixe de réduction"
    )

    # Pour "buy_x_get_y"
    buy_quantity = models.IntegerField(null=True, blank=True, help_text="Quantité à acheter")
    get_quantity = models.IntegerField(null=True, blank=True, help_text="Quantité gratuite")

    # Articles concernés
    applicable_items = models.ManyToManyField(
        'restaurants.MenuItem',
        blank=True,
        related_name='promotions'
    )

    # Validité
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    # Jours de la semaine applicables (format JSON: [0,1,2,3,4,5,6] où 0=Lundi)
    applicable_days = models.JSONField(
        default=list,
        blank=True,
        help_text="Jours de la semaine où la promotion est active"
    )

    # Heures applicables
    start_time = models.TimeField(null=True, blank=True, help_text="Heure de début (ex: happy hour)")
    end_time = models.TimeField(null=True, blank=True, help_text="Heure de fin")

    # Priorité (pour gérer les promotions multiples)
    priority = models.IntegerField(default=0, help_text="Plus élevé = plus prioritaire")

    # Image promotionnelle
    image = models.ImageField(upload_to='promotions/', blank=True)

    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    def is_valid_now(self):
        """Vérifie si la promotion est valide maintenant"""
        from django.utils import timezone
        now = timezone.now()

        if not self.is_active:
            return False

        if now < self.valid_from or now > self.valid_until:
            return False

        # Vérifier le jour de la semaine
        if self.applicable_days and now.weekday() not in self.applicable_days:
            return False

        # Vérifier l'heure
        if self.start_time and self.end_time:
            current_time = now.time()
            if not (self.start_time <= current_time <= self.end_time):
                return False

        return True
