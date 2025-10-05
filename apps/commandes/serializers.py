from rest_framework import serializers
from .models import Order, OrderItem
from apps.restaurants.serializers import MenuItemSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'menu_item', 'menu_item_details', 'quantity',
            'unit_price', 'total_price', 'selected_options', 'special_instructions'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'restaurant', 'delivery_address', 'delivery_latitude',
            'delivery_longitude', 'payment_method', 'customer_notes', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        subtotal = 0
        for item_data in items_data:
            menu_item = item_data['menu_item']
            quantity = item_data['quantity']
            unit_price = menu_item.price

            OrderItem.objects.create(
                order=order,
                unit_price=unit_price,
                **item_data
            )
            subtotal += unit_price * quantity

        # Calcul des totaux
        order.subtotal = subtotal
        order.delivery_fee = order.restaurant.delivery_fee
        order.tax = subtotal * 0.1  # 10% de taxe
        order.total_amount = subtotal + order.delivery_fee + order.tax
        order.save()

        return order


class OrderListSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    restaurant_image = serializers.ImageField(source='restaurant.image', read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'restaurant_name', 'restaurant_image',
            'total_amount', 'estimated_delivery_time', 'created_at', 'items_count'
        ]

    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant_details = serializers.SerializerMethodField()
    tracking = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'restaurant_details', 'items',
            'subtotal', 'delivery_fee', 'tax', 'total_amount', 'payment_method',
            'payment_status', 'delivery_address', 'customer_notes',
            'estimated_delivery_time', 'actual_delivery_time', 'tracking',
            'created_at', 'updated_at'
        ]

    def get_restaurant_details(self, obj):
        return {
            'id': obj.restaurant.id,
            'name': obj.restaurant.name,
            'image': obj.restaurant.image.url if obj.restaurant.image else None,
            'phone_number': str(obj.restaurant.phone_number),
            'address': obj.restaurant.address
        }

    def get_tracking(self, obj):
        if hasattr(obj, 'tracking'):
            return {
                'current_latitude': obj.tracking.current_latitude,
                'current_longitude': obj.tracking.current_longitude,
                'estimated_arrival': obj.tracking.estimated_arrival,
                'distance_remaining_km': obj.tracking.distance_remaining_km
            }
        return None