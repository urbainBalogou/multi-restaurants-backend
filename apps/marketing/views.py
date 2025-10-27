from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Count, Q
from .models import (
    RestaurantAdvertisement,
    SocialMediaShare,
    ShareTemplate,
    NewsletterSubscription,
    PushNotificationCampaign
)
from .serializers import (
    RestaurantAdvertisementSerializer,
    SocialMediaShareSerializer,
    ShareTemplateSerializer,
    NewsletterSubscriptionSerializer,
    PushNotificationCampaignSerializer,
    QuickShareSerializer,
    ShareAnalyticsSerializer
)
import logging

logger = logging.getLogger(__name__)


class RestaurantAdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les publicités des restaurants
    """
    queryset = RestaurantAdvertisement.objects.all()
    serializer_class = RestaurantAdvertisementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            # Les restaurants ne voient que leurs propres publicités
            return self.queryset.filter(restaurant__owner=user)
        return self.queryset
    
    @action(detail=True, methods=['post'])
    def record_impression(self, request, pk=None):
        """Enregistrer une impression de publicité"""
        ad = self.get_object()
        ad.impressions += 1
        ad.save(update_fields=['impressions'])
        return Response({'status': 'impression recorded'})
    
    @action(detail=True, methods=['post'])
    def record_click(self, request, pk=None):
        """Enregistrer un clic sur une publicité"""
        ad = self.get_object()
        ad.clicks += 1
        ad.save(update_fields=['clicks'])
        return Response({'status': 'click recorded'})
    
    @action(detail=True, methods=['post'])
    def record_conversion(self, request, pk=None):
        """Enregistrer une conversion (commande)"""
        ad = self.get_object()
        ad.conversions += 1
        ad.save(update_fields=['conversions'])
        return Response({'status': 'conversion recorded'})
    
    @action(detail=False, methods=['get'])
    def active_ads(self, request):
        """Obtenir toutes les publicités actives"""
        now = timezone.now()
        active_ads = self.get_queryset().filter(
            status='active',
            start_date__lte=now,
            end_date__gte=now
        )
        
        # Filtrage par localisation si fourni
        city = request.query_params.get('city')
        if city:
            active_ads = active_ads.filter(
                Q(target_cities__contains=[city]) | Q(target_cities=[])
            )
        
        serializer = self.get_serializer(active_ads, many=True)
        return Response(serializer.data)


class SocialMediaShareViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les partages sur les réseaux sociaux
    """
    queryset = SocialMediaShare.objects.all()
    serializer_class = SocialMediaShareSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            return self.queryset.filter(restaurant__owner=user)
        return self.queryset.filter(shared_by=user)
    
    def perform_create(self, serializer):
        serializer.save(shared_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def quick_share(self, request):
        """Partager rapidement un restaurant ou article"""
        serializer = QuickShareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        platform = data['platform']
        share_type = data['share_type']
        
        # Récupérer les données en fonction du type
        from apps.restaurants.models import Restaurant, MenuItem
        from apps.promotions.models import Promotion
        
        restaurant_id = request.data.get('restaurant_id')
        restaurant = Restaurant.objects.get(id=restaurant_id)
        
        # Construire le message et le lien
        if share_type == 'restaurant':
            title = f"Découvrez {restaurant.name}"
            message = data.get('custom_message', 
                f"Je vous recommande {restaurant.name} ! {restaurant.description}")
            share_url = f"https://app.multirestaurants.com/restaurant/{restaurant.id}"
            image_url = restaurant.image.url if restaurant.image else ""
            
        elif share_type == 'menu_item':
            menu_item_id = data.get('menu_item_id')
            menu_item = MenuItem.objects.get(id=menu_item_id)
            title = f"{menu_item.name} chez {restaurant.name}"
            message = data.get('custom_message',
                f"J'ai adoré {menu_item.name} ! {menu_item.description} - {menu_item.price}€")
            share_url = f"https://app.multirestaurants.com/restaurant/{restaurant.id}/item/{menu_item.id}"
            image_url = menu_item.image.url if menu_item.image else ""
            
        elif share_type == 'promotion':
            promotion_id = data.get('promotion_id')
            promotion = Promotion.objects.get(id=promotion_id)
            title = f"Promotion : {promotion.name}"
            message = data.get('custom_message',
                f"Super promo chez {restaurant.name} : {promotion.description}")
            share_url = f"https://app.multirestaurants.com/restaurant/{restaurant.id}/promotion/{promotion.id}"
            image_url = promotion.image.url if promotion.image else ""
        
        # Créer le partage
        share = SocialMediaShare.objects.create(
            restaurant=restaurant,
            platform=platform,
            share_type=share_type,
            menu_item_id=data.get('menu_item_id'),
            promotion_id=data.get('promotion_id'),
            title=title,
            message=message,
            image_url=image_url,
            share_url=share_url,
            shared_by=request.user
        )
        
        # Retourner les données de partage formatées pour chaque plateforme
        response_data = {
            'id': share.id,
            'platform': platform,
            'share_url': share_url,
            'title': title,
            'message': message,
            'image_url': image_url,
        }
        
        # Formater pour WhatsApp
        if platform == 'whatsapp':
            whatsapp_message = f"{title}\n\n{message}\n\n{share_url}"
            response_data['whatsapp_url'] = f"https://wa.me/?text={whatsapp_message}"
        
        # Formater pour Facebook
        elif platform == 'facebook':
            response_data['facebook_url'] = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def record_view(self, request, pk=None):
        """Enregistrer une vue du contenu partagé"""
        share = self.get_object()
        share.views += 1
        share.save(update_fields=['views'])
        return Response({'status': 'view recorded'})
    
    @action(detail=True, methods=['post'])
    def record_click(self, request, pk=None):
        """Enregistrer un clic sur le lien partagé"""
        share = self.get_object()
        share.clicks += 1
        share.save(update_fields=['clicks'])
        return Response({'status': 'click recorded'})
    
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Obtenir les statistiques de partage pour un restaurant"""
        user = request.user
        restaurant_id = request.query_params.get('restaurant_id')
        
        if user.user_type == 'restaurant':
            shares = self.queryset.filter(restaurant_id=restaurant_id, restaurant__owner=user)
        else:
            return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        
        analytics_data = shares.aggregate(
            total_shares=Count('id'),
            total_views=Sum('views'),
            total_clicks=Sum('clicks'),
            total_re_shares=Sum('shares_count')
        )
        
        # Statistiques par plateforme
        by_platform = {}
        for platform in ['whatsapp', 'facebook', 'instagram', 'twitter', 'in_app']:
            platform_shares = shares.filter(platform=platform)
            by_platform[platform] = {
                'count': platform_shares.count(),
                'views': platform_shares.aggregate(Sum('views'))['views__sum'] or 0,
                'clicks': platform_shares.aggregate(Sum('clicks'))['clicks__sum'] or 0,
            }
        
        # Statistiques par type
        by_type = {}
        for share_type in ['restaurant', 'menu_item', 'promotion']:
            type_shares = shares.filter(share_type=share_type)
            by_type[share_type] = {
                'count': type_shares.count(),
                'views': type_shares.aggregate(Sum('views'))['views__sum'] or 0,
                'clicks': type_shares.aggregate(Sum('clicks'))['clicks__sum'] or 0,
            }
        
        analytics_data['by_platform'] = by_platform
        analytics_data['by_type'] = by_type
        analytics_data['conversion_rate'] = (
            (analytics_data['total_clicks'] / analytics_data['total_views'] * 100)
            if analytics_data['total_views'] else 0
        )
        
        serializer = ShareAnalyticsSerializer(analytics_data)
        return Response(serializer.data)


class ShareTemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les templates de partage
    """
    queryset = ShareTemplate.objects.all()
    serializer_class = ShareTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            return self.queryset.filter(restaurant__owner=user)
        return self.queryset.none()
    
    @action(detail=True, methods=['post'])
    def generate_share(self, request, pk=None):
        """Générer un partage à partir d'un template"""
        template = self.get_object()
        
        # Variables pour le template
        restaurant = template.restaurant
        menu_item_id = request.data.get('menu_item_id')
        
        context = {
            'restaurant_name': restaurant.name,
            'address': restaurant.address,
        }
        
        if menu_item_id:
            from apps.restaurants.models import MenuItem
            menu_item = MenuItem.objects.get(id=menu_item_id)
            context.update({
                'item_name': menu_item.name,
                'price': menu_item.price,
            })
        
        # Remplacer les variables dans le template
        title = template.title_template.format(**context)
        message = template.message_template.format(**context)
        
        # Ajouter les hashtags
        if template.hashtags:
            hashtags_str = ' '.join([f"#{tag}" for tag in template.hashtags])
            message = f"{message}\n\n{hashtags_str}"
        
        return Response({
            'title': title,
            'message': message,
            'image_url': template.default_image.url if template.default_image else None,
        })


class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les abonnements aux newsletters
    """
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            return self.queryset.filter(restaurant__owner=user)
        return self.queryset.filter(user=user)
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """S'abonner à la newsletter d'un restaurant"""
        restaurant_id = request.data.get('restaurant_id')
        
        subscription, created = NewsletterSubscription.objects.get_or_create(
            restaurant_id=restaurant_id,
            user=request.user,
            defaults={
                'email': request.user.email,
                'is_active': True,
            }
        )
        
        if not created and not subscription.is_active:
            subscription.is_active = True
            subscription.unsubscribed_at = None
            subscription.save()
        
        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def unsubscribe(self, request, pk=None):
        """Se désabonner d'une newsletter"""
        subscription = self.get_object()
        subscription.is_active = False
        subscription.unsubscribed_at = timezone.now()
        subscription.save()
        
        return Response({'status': 'unsubscribed'})


class PushNotificationCampaignViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les campagnes de notifications push
    """
    queryset = PushNotificationCampaign.objects.all()
    serializer_class = PushNotificationCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'restaurant':
            return self.queryset.filter(restaurant__owner=user)
        return self.queryset.none()
    
    @action(detail=True, methods=['post'])
    def send_now(self, request, pk=None):
        """Envoyer la campagne immédiatement"""
        campaign = self.get_object()
        
        if campaign.status != 'draft' and campaign.status != 'scheduled':
            return Response(
                {'error': 'Campaign already sent'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # TODO: Implémenter l'envoi réel des notifications avec Firebase
        # Pour l'instant, on simule
        campaign.status = 'sent'
        campaign.sent_at = timezone.now()
        campaign.save()
        
        logger.info(f"Push campaign {campaign.id} sent for restaurant {campaign.restaurant.name}")
        
        return Response({'status': 'sent', 'sent_at': campaign.sent_at})
    
    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        """Planifier l'envoi de la campagne"""
        campaign = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        
        campaign.scheduled_at = scheduled_at
        campaign.status = 'scheduled'
        campaign.save()
        
        # TODO: Créer une tâche Celery pour l'envoi planifié
        
        return Response({'status': 'scheduled', 'scheduled_at': campaign.scheduled_at})
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annuler une campagne planifiée"""
        campaign = self.get_object()
        
        if campaign.status != 'scheduled':
            return Response(
                {'error': 'Only scheduled campaigns can be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        campaign.status = 'cancelled'
        campaign.save()
        
        return Response({'status': 'cancelled'})
