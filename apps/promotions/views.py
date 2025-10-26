from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Coupon, CouponUsage, Promotion
from .serializers import (
    CouponSerializer, CouponUsageSerializer,
    PromotionSerializer, ValidateCouponSerializer
)
from apps.restaurants.models import Restaurant
import logging

logger = logging.getLogger(__name__)


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['discount_type', 'is_active']
    search_fields = ['code', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer uniquement les coupons actifs et valides pour les utilisateurs non-admin
        if not self.request.user.is_staff:
            now = timezone.now()
            queryset = queryset.filter(
                is_active=True,
                valid_from__lte=now,
                valid_until__gte=now
            )
        return queryset

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def validate(self, request):
        """Valider un code promo"""
        serializer = ValidateCouponSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data['code']
        order_amount = serializer.validated_data.get('order_amount', 0)
        restaurant_id = serializer.validated_data.get('restaurant_id')

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({
                "valid": False,
                "message": "Code promo invalide"
            }, status=status.HTTP_404_NOT_FOUND)

        # Vérifier la validité
        is_valid, message = coupon.is_valid()
        if not is_valid:
            return Response({
                "valid": False,
                "message": message
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier le montant minimum
        if order_amount < coupon.min_order_amount:
            return Response({
                "valid": False,
                "message": f"Montant minimum de commande: {coupon.min_order_amount}€"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier le restaurant applicable
        if restaurant_id and coupon.applicable_restaurants.exists():
            if not coupon.applicable_restaurants.filter(id=restaurant_id).exists():
                return Response({
                    "valid": False,
                    "message": "Ce coupon n'est pas applicable à ce restaurant"
                }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier l'utilisateur autorisé
        if coupon.allowed_users.exists():
            if request.user not in coupon.allowed_users.all():
                return Response({
                    "valid": False,
                    "message": "Ce coupon ne vous est pas destiné"
                }, status=status.HTTP_403_FORBIDDEN)

        # Vérifier la limite d'utilisation par utilisateur
        user_usage_count = CouponUsage.objects.filter(
            coupon=coupon,
            user=request.user
        ).count()

        if user_usage_count >= coupon.usage_limit_per_user:
            return Response({
                "valid": False,
                "message": "Vous avez déjà utilisé ce coupon le nombre maximum de fois"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculer la réduction
        discount_amount = coupon.calculate_discount(order_amount) if order_amount > 0 else 0

        return Response({
            "valid": True,
            "message": "Code promo valide",
            "coupon": CouponSerializer(coupon).data,
            "discount_amount": discount_amount,
            "free_delivery": coupon.discount_type == 'free_delivery'
        })

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_coupons(self, request):
        """Récupère les coupons disponibles pour l'utilisateur connecté"""
        now = timezone.now()
        coupons = Coupon.objects.filter(
            is_active=True,
            valid_from__lte=now,
            valid_until__gte=now
        ).filter(
            # Soit aucun utilisateur spécifique, soit l'utilisateur connecté
            models.Q(allowed_users__isnull=True) |
            models.Q(allowed_users=request.user)
        ).distinct()

        serializer = self.get_serializer(coupons, many=True)
        return Response(serializer.data)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['restaurant', 'promotion_type', 'is_active']
    search_fields = ['name', 'description']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer uniquement les promotions actives pour les utilisateurs non-admin
        if not self.request.user.is_staff:
            now = timezone.now()
            queryset = queryset.filter(
                is_active=True,
                valid_from__lte=now,
                valid_until__gte=now
            )
        return queryset

    @action(detail=False, methods=['get'])
    def active_now(self, request):
        """Récupère toutes les promotions actuellement actives"""
        promotions = [p for p in self.get_queryset() if p.is_valid_now()]
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_restaurant(self, request):
        """Récupère les promotions d'un restaurant spécifique"""
        restaurant_id = request.query_params.get('restaurant_id')
        if not restaurant_id:
            return Response({
                "error": "restaurant_id est requis"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({
                "error": "Restaurant non trouvé"
            }, status=status.HTTP_404_NOT_FOUND)

        promotions = [
            p for p in self.get_queryset().filter(restaurant=restaurant)
            if p.is_valid_now()
        ]
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)


class CouponUsageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CouponUsage.objects.all()
    serializer_class = CouponUsageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['coupon', 'user', 'order']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Les utilisateurs ne peuvent voir que leurs propres utilisations
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
