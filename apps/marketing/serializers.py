from rest_framework import serializers
from .models import (
    RestaurantAdvertisement,
    SocialMediaShare,
    ShareTemplate,
    NewsletterSubscription,
    PushNotificationCampaign
)
from apps.restaurants.serializers import RestaurantSerializer
from apps.authentication.serializers import UserSerializer


class RestaurantAdvertisementSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    click_through_rate = serializers.FloatField(read_only=True)
    conversion_rate = serializers.FloatField(read_only=True)
    total_cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = RestaurantAdvertisement
        fields = [
            'id', 'restaurant', 'restaurant_name', 'ad_type', 'title', 'description',
            'image', 'target_cities', 'target_age_min', 'target_age_max',
            'start_date', 'end_date', 'status', 'budget', 'cost_per_click',
            'impressions', 'clicks', 'conversions', 'click_through_rate',
            'conversion_rate', 'total_cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['impressions', 'clicks', 'conversions', 'created_at', 'updated_at']


class SocialMediaShareSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    shared_by_username = serializers.CharField(source='shared_by.username', read_only=True, allow_null=True)
    
    class Meta:
        model = SocialMediaShare
        fields = [
            'id', 'restaurant', 'restaurant_name', 'platform', 'share_type',
            'menu_item', 'promotion', 'title', 'message', 'image_url',
            'share_url', 'views', 'clicks', 'shares_count', 'shared_by',
            'shared_by_username', 'shared_at'
        ]
        read_only_fields = ['views', 'clicks', 'shares_count', 'shared_at']


class ShareTemplateSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    
    class Meta:
        model = ShareTemplate
        fields = [
            'id', 'restaurant', 'restaurant_name', 'name', 'platform',
            'title_template', 'message_template', 'default_image',
            'hashtags', 'is_active', 'created_at'
        ]
        read_only_fields = ['created_at']


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = NewsletterSubscription
        fields = [
            'id', 'restaurant', 'restaurant_name', 'user', 'user_email',
            'email', 'is_active', 'notify_new_items', 'notify_promotions',
            'notify_events', 'subscribed_at', 'unsubscribed_at'
        ]
        read_only_fields = ['subscribed_at', 'unsubscribed_at']


class PushNotificationCampaignSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    open_rate = serializers.FloatField(read_only=True)
    click_rate = serializers.FloatField(read_only=True)
    
    class Meta:
        model = PushNotificationCampaign
        fields = [
            'id', 'restaurant', 'restaurant_name', 'title', 'message',
            'target_all_customers', 'target_favorites', 'target_previous_orders',
            'status', 'scheduled_at', 'sent_at', 'action_type', 'action_data',
            'recipients_count', 'delivered_count', 'opened_count', 'clicked_count',
            'open_rate', 'click_rate', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'sent_at', 'recipients_count', 'delivered_count', 'opened_count',
            'clicked_count', 'created_at', 'updated_at'
        ]


# Serializers pour le partage rapide
class QuickShareSerializer(serializers.Serializer):
    """Pour partager rapidement un restaurant ou article"""
    platform = serializers.ChoiceField(choices=SocialMediaShare.PLATFORM_CHOICES)
    share_type = serializers.ChoiceField(choices=SocialMediaShare.SHARE_TYPE)
    menu_item_id = serializers.IntegerField(required=False, allow_null=True)
    promotion_id = serializers.IntegerField(required=False, allow_null=True)
    custom_message = serializers.CharField(required=False, allow_blank=True)


class ShareAnalyticsSerializer(serializers.Serializer):
    """Pour les statistiques de partage"""
    total_shares = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_clicks = serializers.IntegerField()
    by_platform = serializers.DictField()
    by_type = serializers.DictField()
    conversion_rate = serializers.FloatField()
