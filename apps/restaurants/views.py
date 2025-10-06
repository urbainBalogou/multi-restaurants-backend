from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from geopy.distance import geodesic
from .models import Restaurant, MenuItem, Category, RestaurantReview
from .serializers import (
    RestaurantListSerializer, RestaurantDetailSerializer,
    MenuItemSerializer, CategorySerializer, RestaurantReviewSerializer, RestaurantCreateSerializer,
    MenuItemBulkCreateSerializer
)
from apps.authentication.models import User
from ..core.permissions import IsRestaurantOwner


class ProximityFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        latitude = request.query_params.get('lat')
        longitude = request.query_params.get('lng')
        radius = request.query_params.get('radius', 10)  # 10km par défaut

        if latitude and longitude:
            user_location = (float(latitude), float(longitude))
            restaurants_with_distance = []

            for restaurant in queryset:
                restaurant_location = (restaurant.latitude, restaurant.longitude)
                distance = geodesic(user_location, restaurant_location).kilometers

                if distance <= float(radius):
                    restaurant.distance_km = round(distance, 2)
                    restaurants_with_distance.append(restaurant)

            # Tri par distance
            restaurants_with_distance.sort(key=lambda x: x.distance_km)
            return restaurants_with_distance

        return queryset


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, ProximityFilterBackend]
    filterset_fields = ['is_accepting_orders']
    search_fields = ['name', 'description']
    ordering_fields = ['average_rating', 'estimated_delivery_time', 'created_at']
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsRestaurantOwner()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == 'create':
            print("données: ", self.request.data)
            return RestaurantCreateSerializer
        elif self.action == 'list':
            return RestaurantListSerializer
        return RestaurantDetailSerializer

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Récupérer l'instance créée
        restaurant = serializer.instance

        # Sérialiser avec le serializer de détail
        detail_serializer = RestaurantDetailSerializer(restaurant, context=self.get_serializer_context())

        return Response({
            "message": "Restaurant créé avec succès",
            "data": detail_serializer.data,
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False  # Désactiver plutôt que supprimer
        instance.save()

    @action(detail=True, methods=['get'])
    def menu(self, request, pk=None):
        """Récupère le menu complet du restaurant"""
        restaurant = self.get_object()
        categories = Category.objects.filter(is_active=True)

        menu_data = []
        for category in categories:
            items = MenuItem.objects.filter(
                restaurant=restaurant,
                category=category,
                is_available=True
            )
            if items.exists():
                menu_data.append({
                    'category': CategorySerializer(category).data,
                    'items': MenuItemSerializer(items, many=True).data
                })

        return Response(menu_data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Récupère les avis du restaurant"""
        restaurant = self.get_object()
        reviews = RestaurantReview.objects.filter(restaurant=restaurant)

        # Pagination
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = RestaurantReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RestaurantReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Restaurants populaires"""
        popular_restaurants = self.get_queryset().filter(
            average_rating__gte=4.0
        ).order_by('-total_reviews')[:10]

        serializer = self.get_serializer(popular_restaurants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>\d+)/restaurants')
    def user_restaurants(self, request, user_id=None):
        """
        Récupère tous les restaurants associés à un utilisateur (propriétaire)
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

        restaurants = self.queryset.filter(owner=user)
        serializer = RestaurantListSerializer(restaurants, many=True)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "restaurants": serializer.data,
            "count": restaurants.count()
        })


class MenuItemViewSet(viewsets.ModelViewSet):  # Changé en ModelViewSet
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['restaurant', 'category', 'is_available']
    search_fields = ['name', 'description']
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsRestaurantOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'create':
            return MenuItemBulkCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_bulk_create(self, serializer):
        menu_items = serializer.save()
        return Response({
            "message": f"{len(menu_items)} menus créés avec succès",
            "created_items": MenuItemSerializer(menu_items, many=True).data
        })

    @action(detail=False, methods=['get'], url_path='user/(?P<user_id>\d+)/menus')
    def user_menus(self, request, user_id=None):
        """
        Récupère tous les menus des restaurants d'un propriétaire
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si l'utilisateur est un propriétaire de restaurant
        restaurants = Restaurant.objects.filter(owner=user, is_active=True)
        if not restaurants.exists():
            return Response(
                {"message": "Cet utilisateur n'est pas propriétaire de restaurant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer tous les menus des restaurants du propriétaire
        menu_items = MenuItem.objects.filter(
            restaurant__in=restaurants,
            is_available=True
        ).select_related('restaurant', 'category')

        serializer = self.get_serializer(menu_items, many=True)

        return Response({
            "owner": user.get_full_name() or user.username,
            "restaurant_count": restaurants.count(),
            "menu_items": serializer.data,
            "total_items": menu_items.count()
        })

    @action(detail=False, methods=['get'], url_path=r'user/(?P<user_id>\d+)/menus')
    def user_menus(self, request, user_id=None):
        """
        Récupère tous les menus des restaurants d'un propriétaire
        """
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Vérifier si l'utilisateur est un propriétaire de restaurant
        restaurants = Restaurant.objects.filter(owner=user, is_active=True)
        if not restaurants.exists():
            return Response(
                {"message": "Cet utilisateur n'est pas propriétaire de restaurant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer tous les menus des restaurants du propriétaire
        menu_items = MenuItem.objects.filter(
            restaurant__in=restaurants,
            is_available=True
        ).select_related('restaurant', 'category')

        serializer = self.get_serializer(menu_items, many=True)

        return Response({
            "owner": user.get_full_name() or user.username,
            "restaurant_count": restaurants.count(),
            "menu_items": serializer.data,
            "total_items": menu_items.count()
        })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], url_path='(?P<id>[^/.]+)/menus')
    def get_category_menus(self, request, id=None):
        try:
            category = Category.objects.get(id=id, is_active=True)
        except Category.DoesNotExist:
            return Response(
                {"message": "Catégorie non trouvée"},
                status=status.HTTP_404_NOT_FOUND
            )

        menus = MenuItem.objects.filter(category=category, is_available=True)
        serializer = MenuItemSerializer(menus, many=True)

        return Response({
            "category": CategorySerializer(category).data,
            "data": serializer.data,
            "count": menus.count()
        })
