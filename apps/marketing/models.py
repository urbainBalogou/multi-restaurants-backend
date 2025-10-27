from django.db import models
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant, MenuItem

User = get_user_model()


class RestaurantAdvertisement(models.Model):
    """Publicités et campagnes marketing pour les restaurants"""
    
    AD_TYPES = (
        ('banner', 'Bannière dans l\'app'),
        ('featured', 'Restaurant mis en avant'),
        ('promotion', 'Promotion spéciale'),
        ('sponsored', 'Résultat sponsorisé'),
    )
    
    AD_STATUS = (
        ('draft', 'Brouillon'),
        ('active', 'Active'),
        ('paused', 'En pause'),
        ('completed', 'Terminée'),
    )
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )
    
    # Type et contenu
    ad_type = models.CharField(max_length=20, choices=AD_TYPES)
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='advertisements/', blank=True)
    
    # Ciblage
    target_cities = models.JSONField(
        default=list,
        blank=True,
        help_text="Villes ciblées (si vide, toutes)"
    )
    target_age_min = models.IntegerField(null=True, blank=True)
    target_age_max = models.IntegerField(null=True, blank=True)
    
    # Période
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=AD_STATUS, default='draft')
    
    # Budget et performance
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Budget total de la campagne (€)"
    )
    cost_per_click = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.50,
        help_text="Coût par clic (€)"
    )
    
    # Métriques
    impressions = models.IntegerField(default=0, verbose_name="Impressions")
    clicks = models.IntegerField(default=0, verbose_name="Clics")
    conversions = models.IntegerField(default=0, verbose_name="Conversions (commandes)")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Publicité"
        verbose_name_plural = "Publicités"
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.title}"
    
    @property
    def click_through_rate(self):
        """Taux de clic"""
        if self.impressions > 0:
            return (self.clicks / self.impressions) * 100
        return 0
    
    @property
    def conversion_rate(self):
        """Taux de conversion"""
        if self.clicks > 0:
            return (self.conversions / self.clicks) * 100
        return 0
    
    @property
    def total_cost(self):
        """Coût total de la campagne"""
        return self.clicks * self.cost_per_click


class SocialMediaShare(models.Model):
    """Partages sur les réseaux sociaux"""
    
    PLATFORM_CHOICES = (
        ('whatsapp', 'WhatsApp'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('in_app', 'Dans l\'application'),
    )
    
    SHARE_TYPE = (
        ('restaurant', 'Restaurant'),
        ('menu_item', 'Article du menu'),
        ('promotion', 'Promotion'),
    )
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='social_shares'
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    share_type = models.CharField(max_length=20, choices=SHARE_TYPE)
    
    # Contenu partagé
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shares'
    )
    promotion = models.ForeignKey(
        'promotions.Promotion',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='shares'
    )
    
    # Contenu du partage
    title = models.CharField(max_length=200)
    message = models.TextField()
    image_url = models.URLField(blank=True)
    share_url = models.URLField(blank=True, verbose_name="Lien de partage")
    
    # Métriques
    views = models.IntegerField(default=0, verbose_name="Vues")
    clicks = models.IntegerField(default=0, verbose_name="Clics")
    shares_count = models.IntegerField(default=0, verbose_name="Partages")
    
    # Utilisateur qui a partagé (si depuis l'app)
    shared_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shares'
    )
    
    shared_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-shared_at']
        verbose_name = "Partage social"
        verbose_name_plural = "Partages sociaux"
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.get_platform_display()}"


class ShareTemplate(models.Model):
    """Templates de partage personnalisables pour les restaurants"""
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='share_templates'
    )
    
    name = models.CharField(max_length=100, verbose_name="Nom du template")
    platform = models.CharField(max_length=20, choices=SocialMediaShare.PLATFORM_CHOICES)
    
    # Template du message
    title_template = models.CharField(
        max_length=200,
        help_text="Variables: {restaurant_name}, {item_name}, {price}, {discount}"
    )
    message_template = models.TextField(
        help_text="Variables: {restaurant_name}, {item_name}, {price}, {discount}, {address}"
    )
    
    # Image par défaut
    default_image = models.ImageField(upload_to='share_templates/', blank=True)
    
    # Hashtags
    hashtags = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de hashtags à ajouter"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['platform', 'name']
        verbose_name = "Template de partage"
        verbose_name_plural = "Templates de partage"
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.name} ({self.get_platform_display()})"


class NewsletterSubscription(models.Model):
    """Abonnements aux newsletters des restaurants"""
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='newsletter_subscriptions'
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='newsletter_subscriptions'
    )
    
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    # Préférences
    notify_new_items = models.BooleanField(default=True, verbose_name="Nouveaux articles")
    notify_promotions = models.BooleanField(default=True, verbose_name="Promotions")
    notify_events = models.BooleanField(default=False, verbose_name="Événements")
    
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['restaurant', 'user']
        ordering = ['-subscribed_at']
        verbose_name = "Abonnement newsletter"
        verbose_name_plural = "Abonnements newsletter"
    
    def __str__(self):
        return f"{self.user.email} - {self.restaurant.name}"


class PushNotificationCampaign(models.Model):
    """Campagnes de notifications push pour les restaurants"""
    
    CAMPAIGN_STATUS = (
        ('draft', 'Brouillon'),
        ('scheduled', 'Planifiée'),
        ('sent', 'Envoyée'),
        ('cancelled', 'Annulée'),
    )
    
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='push_campaigns'
    )
    
    title = models.CharField(max_length=100, verbose_name="Titre")
    message = models.TextField(max_length=200, verbose_name="Message")
    
    # Ciblage
    target_all_customers = models.BooleanField(
        default=False,
        verbose_name="Tous les clients"
    )
    target_favorites = models.BooleanField(
        default=False,
        verbose_name="Clients ayant mis en favori"
    )
    target_previous_orders = models.BooleanField(
        default=False,
        verbose_name="Clients ayant déjà commandé"
    )
    
    # Période
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS, default='draft')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Lien d'action
    action_type = models.CharField(
        max_length=20,
        choices=(
            ('menu', 'Ouvrir le menu'),
            ('promotion', 'Voir la promotion'),
            ('order', 'Commander'),
        ),
        default='menu'
    )
    action_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Données pour l'action (ex: promotion_id)"
    )
    
    # Métriques
    recipients_count = models.IntegerField(default=0, verbose_name="Destinataires")
    delivered_count = models.IntegerField(default=0, verbose_name="Délivrées")
    opened_count = models.IntegerField(default=0, verbose_name="Ouvertes")
    clicked_count = models.IntegerField(default=0, verbose_name="Cliquées")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Campagne push"
        verbose_name_plural = "Campagnes push"
    
    def __str__(self):
        return f"{self.restaurant.name} - {self.title}"
    
    @property
    def open_rate(self):
        """Taux d'ouverture"""
        if self.delivered_count > 0:
            return (self.opened_count / self.delivered_count) * 100
        return 0
    
    @property
    def click_rate(self):
        """Taux de clic"""
        if self.opened_count > 0:
            return (self.clicked_count / self.opened_count) * 100
        return 0
