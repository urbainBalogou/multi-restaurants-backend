from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantAdvertisementViewSet,
    SocialMediaShareViewSet,
    ShareTemplateViewSet,
    NewsletterSubscriptionViewSet,
    PushNotificationCampaignViewSet
)

router = DefaultRouter()
router.register(r'advertisements', RestaurantAdvertisementViewSet, basename='advertisement')
router.register(r'shares', SocialMediaShareViewSet, basename='share')
router.register(r'share-templates', ShareTemplateViewSet, basename='share-template')
router.register(r'newsletter-subscriptions', NewsletterSubscriptionViewSet, basename='newsletter-subscription')
router.register(r'push-campaigns', PushNotificationCampaignViewSet, basename='push-campaign')

urlpatterns = [
    path('', include(router.urls)),
]
