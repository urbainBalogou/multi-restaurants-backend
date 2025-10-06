from rest_framework import serializers
from .models import Restaurant, MenuItem, Category, RestaurantReview
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'is_active']


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'image', 'is_available',
            'preparation_time', 'has_options', 'options', 'calories', 'allergens',
            'category', 'category_name', 'restaurant', 'order_count', 'average_rating'
        ]


class RestaurantListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des restaurants (données minimales)"""
    distance_km = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'image', 'average_rating', 'total_reviews',
            'delivery_fee', 'estimated_delivery_time', 'is_accepting_orders',
            'distance_km'
        ]

    def get_distance_km(self, obj):
        # Calculé par la vue selon la position de l'utilisateur
        return getattr(obj, 'distance_km', None)


class RestaurantDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour un restaurant"""
    menu_items = MenuItemSerializer(many=True, read_only=True)
    reviews_count = serializers.IntegerField(source='total_reviews', read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'description', 'image', 'address', 'phone_number',
            'opening_hours', 'is_active', 'is_accepting_orders', 'average_rating',
            'total_reviews', 'reviews_count', 'delivery_fee', 'free_delivery_threshold',
            'delivery_radius_km', 'estimated_delivery_time', 'menu_items'
        ]


class RestaurantReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = RestaurantReview
        fields = ['id', 'rating', 'comment', 'created_at', 'customer_name']
        read_only_fields = ['customer']


# Dans serializers.py
class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'description', 'address', 'latitude', 'longitude',
            'phone_number', 'email', 'opening_hours', 'delivery_fee',
            'free_delivery_threshold', 'delivery_radius_km',
            'estimated_delivery_time', 'is_accepting_orders'
        ]
        read_only_fields = ('owner', 'average_rating', 'total_reviews', 'is_active')

    def validate(self, data):
        if self.context['request'].user.user_type != 'restaurant':
            raise serializers.ValidationError("Seuls les restaurateurs peuvent créer/modifier des restaurants")
        return data


class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Extraction des restaurants vérifiés
        restaurants = {
            data['restaurant_id']: Restaurant.objects.get(id=data['restaurant_id'])
            for data in validated_data
        }

        # Création des menu items en bulk
        items = [
            MenuItem(
                restaurant=restaurants[data['restaurant_id']],
                **{k: v for k, v in data.items() if k != 'restaurant_id'}
            ) for data in validated_data
        ]

        return MenuItem.objects.bulk_create(items)


class MenuItemBulkCreateSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = '__all__'
        list_serializer_class = BulkCreateListSerializer

    def validate_restaurant_id(self, value):
        # Vérifie que le restaurant appartient à l'utilisateur
        if not Restaurant.objects.filter(id=value, owner=self.context['request'].user).exists():
            raise serializers.ValidationError("Vous n'êtes pas propriétaire de ce restaurant")
        return value




