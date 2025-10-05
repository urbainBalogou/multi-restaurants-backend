from rest_framework import serializers
from .models import DeliveryTracking, DeliveryZone
from apps.commandes.serializers import OrderListSerializer
from apps.restaurants.serializers import RestaurantSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class DeliveryTrackingSerializer(serializers.ModelSerializer):
    order = OrderListSerializer(read_only=True)
    driver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DeliveryTracking
        fields = [
            'id',
            'order',
            'driver',
            'current_latitude',
            'current_longitude',
            'last_location_update',
            'estimated_arrival',
            'distance_remaining_km',
            'picked_up_at',
            'delivered_at',
            'created_at',
            'updated_at',
        ]


class DeliveryTrackingUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour la position et le statut du livreur"""
    class Meta:
        model = DeliveryTracking
        fields = [
            'current_latitude',
            'current_longitude',
            'last_location_update',
            'estimated_arrival',
            'distance_remaining_km',
            'picked_up_at',
            'delivered_at',
        ]


class DeliveryZoneSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = DeliveryZone
        fields = [
            'id',
            'name',
            'restaurant',
            'coordinates',
            'delivery_fee',
            'estimated_time',
            'is_active',
        ]
