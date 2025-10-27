from django.contrib import admin
from .models import (
    RestaurantAdvertisement,
    SocialMediaShare,
    ShareTemplate,
    NewsletterSubscription,
    PushNotificationCampaign
)


@admin.register(RestaurantAdvertisement)
class RestaurantAdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant', 'title', 'ad_type', 'status', 'start_date', 'end_date',
        'impressions', 'clicks', 'conversions', 'total_cost'
    ]
    list_filter = ['ad_type', 'status', 'start_date']
    search_fields = ['restaurant__name', 'title', 'description']
    date_hierarchy = 'start_date'
    readonly_fields = ['impressions', 'clicks', 'conversions', 'click_through_rate', 'conversion_rate', 'total_cost']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('restaurant', 'ad_type', 'title', 'description', 'image')
        }),
        ('Ciblage', {
            'fields': ('target_cities', 'target_age_min', 'target_age_max')
        }),
        ('Période et statut', {
            'fields': ('start_date', 'end_date', 'status')
        }),
        ('Budget', {
            'fields': ('budget', 'cost_per_click', 'total_cost')
        }),
        ('Métriques', {
            'fields': ('impressions', 'clicks', 'conversions', 'click_through_rate', 'conversion_rate')
        }),
    )


@admin.register(SocialMediaShare)
class SocialMediaShareAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant', 'platform', 'share_type', 'shared_by',
        'views', 'clicks', 'shares_count', 'shared_at'
    ]
    list_filter = ['platform', 'share_type', 'shared_at']
    search_fields = ['restaurant__name', 'title', 'message']
    date_hierarchy = 'shared_at'
    readonly_fields = ['shared_at']


@admin.register(ShareTemplate)
class ShareTemplateAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'name', 'platform', 'is_active', 'created_at']
    list_filter = ['platform', 'is_active']
    search_fields = ['restaurant__name', 'name']


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'restaurant', 'email', 'is_active',
        'notify_new_items', 'notify_promotions', 'subscribed_at'
    ]
    list_filter = ['is_active', 'notify_new_items', 'notify_promotions', 'notify_events']
    search_fields = ['user__email', 'restaurant__name', 'email']
    date_hierarchy = 'subscribed_at'


@admin.register(PushNotificationCampaign)
class PushNotificationCampaignAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant', 'title', 'status', 'scheduled_at', 'sent_at',
        'recipients_count', 'delivered_count', 'opened_count', 'open_rate'
    ]
    list_filter = ['status', 'action_type', 'scheduled_at']
    search_fields = ['restaurant__name', 'title', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = [
        'recipients_count', 'delivered_count', 'opened_count', 'clicked_count',
        'open_rate', 'click_rate', 'sent_at'
    ]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('restaurant', 'title', 'message')
        }),
        ('Ciblage', {
            'fields': ('target_all_customers', 'target_favorites', 'target_previous_orders')
        }),
        ('Planification', {
            'fields': ('status', 'scheduled_at', 'sent_at')
        }),
        ('Action', {
            'fields': ('action_type', 'action_data')
        }),
        ('Métriques', {
            'fields': ('recipients_count', 'delivered_count', 'opened_count', 'clicked_count', 'open_rate', 'click_rate')
        }),
    )
