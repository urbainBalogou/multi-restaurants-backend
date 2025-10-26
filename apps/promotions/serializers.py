from rest_framework import serializers
from .models import Coupon, CouponUsage, Promotion
from apps.restaurants.serializers import MenuItemSerializer, RestaurantListSerializer


class CouponSerializer(serializers.ModelSerializer):
    is_currently_valid = serializers.SerializerMethodField()
    applicable_restaurants_data = RestaurantListSerializer(source='applicable_restaurants', many=True, read_only=True)

    class Meta:
        model = Coupon
        fields = [
            'id', 'code', 'description', 'discount_type', 'discount_value',
            'min_order_amount', 'max_discount_amount',
            'valid_from', 'valid_until', 'is_active',
            'usage_limit', 'usage_limit_per_user', 'usage_count',
            'applicable_restaurants', 'applicable_restaurants_data',
            'allowed_users', 'is_currently_valid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['usage_count', 'created_at', 'updated_at']

    def get_is_currently_valid(self, obj):
        is_valid, message = obj.is_valid()
        return {"valid": is_valid, "message": message}


class CouponUsageSerializer(serializers.ModelSerializer):
    coupon_code = serializers.CharField(source='coupon.code', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = CouponUsage
        fields = [
            'id', 'coupon', 'coupon_code', 'user', 'user_username',
            'order', 'discount_amount', 'used_at'
        ]
        read_only_fields = ['used_at']


class PromotionSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    applicable_items_data = MenuItemSerializer(source='applicable_items', many=True, read_only=True)
    is_valid_now = serializers.BooleanField(read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id', 'restaurant', 'restaurant_name', 'name', 'description',
            'promotion_type', 'discount_value',
            'buy_quantity', 'get_quantity',
            'applicable_items', 'applicable_items_data',
            'valid_from', 'valid_until', 'is_active',
            'applicable_days', 'start_time', 'end_time',
            'priority', 'image', 'is_valid_now',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_valid_now'] = instance.is_valid_now()
        return representation


class ValidateCouponSerializer(serializers.Serializer):
    """Serializer pour valider un coupon"""
    code = serializers.CharField(max_length=50)
    order_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    restaurant_id = serializers.IntegerField(required=False)
