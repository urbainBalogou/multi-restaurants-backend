from django.contrib import admin
from .models import Coupon, CouponUsage, Promotion


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value', 'is_active',
        'valid_from', 'valid_until', 'usage_count', 'usage_limit'
    ]
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    filter_horizontal = ['applicable_restaurants', 'allowed_users']
    readonly_fields = ['usage_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Informations de base', {
            'fields': ('code', 'description', 'is_active')
        }),
        ('Type de réduction', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Conditions', {
            'fields': ('min_order_amount',)
        }),
        ('Validité', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Limitations', {
            'fields': ('usage_limit', 'usage_limit_per_user', 'usage_count')
        }),
        ('Restrictions', {
            'fields': ('applicable_restaurants', 'allowed_users'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ['coupon', 'user', 'order', 'discount_amount', 'used_at']
    list_filter = ['used_at', 'coupon']
    search_fields = ['coupon__code', 'user__username', 'user__email']
    readonly_fields = ['used_at']

    def has_add_permission(self, request):
        # Empêcher la création manuelle d'utilisations
        return False


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'restaurant', 'promotion_type', 'discount_value',
        'is_active', 'valid_from', 'valid_until', 'priority'
    ]
    list_filter = ['promotion_type', 'is_active', 'restaurant', 'valid_from', 'valid_until']
    search_fields = ['name', 'description', 'restaurant__name']
    filter_horizontal = ['applicable_items']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informations de base', {
            'fields': ('restaurant', 'name', 'description', 'is_active', 'priority')
        }),
        ('Type de promotion', {
            'fields': ('promotion_type', 'discount_value')
        }),
        ('Buy X Get Y', {
            'fields': ('buy_quantity', 'get_quantity'),
            'classes': ('collapse',)
        }),
        ('Articles applicables', {
            'fields': ('applicable_items',)
        }),
        ('Validité', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Planning', {
            'fields': ('applicable_days', 'start_time', 'end_time'),
            'classes': ('collapse',)
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
