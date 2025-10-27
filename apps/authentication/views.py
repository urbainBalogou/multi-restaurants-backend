from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from .models import User, DriverProfile
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UtilisateurSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        login_data = {
            'identifiant': request.data.get('identifiant'),
            'password': request.data.get('password')
        }

        serializer = LoginSerializer(data=login_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Sérialisation des données utilisateur
        user_serializer = UtilisateurSerializer(user)
        refresh = RefreshToken.for_user(user)
        user_data = user_serializer.data
        user_data['api_token'] = str(refresh.access_token)
        return Response({
                'data': user_data,
            }, status=status.HTTP_200_OK)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        logger.info("Début du processus d'inscription")

        # Vérification des champs requis
        required_fields = ['username', 'email', 'password', 'user_type']
        missing_fields = [field for field in required_fields if field not in request.data]

        if missing_fields:
            logger.warning(f"Champs requis manquants: {missing_fields}")

        # Création du serializer
        serializer = RegisterSerializer(data=request.data)

        # Validation
        if serializer.is_valid():
            logger.info("Validation des données réussie")

            try:
                # Création de l'utilisateur
                user = serializer.save()
                logger.info(f"Utilisateur créé avec succès: {user.email} (ID: {user.id})")

                refresh = RefreshToken.for_user(user)
                user_data = UtilisateurSerializer(user).data
                user_data['api_token'] = str(refresh.access_token)

                return Response({
                    "message": "Inscription réussie",
                    "data": user_data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Erreur lors de la création de l'utilisateur: {e}", exc_info=True)

                return Response({
                    "message": "Erreur lors de la création de l'utilisateur",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            logger.warning(f"Erreurs de validation: {serializer.errors}")

            # Retourner les erreurs détaillées
            return Response({
                "message": "Erreurs de validation",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


"""class GoogleAuthAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        try:
            # Vérifier le token avec Google
            id_info = id_token.verify_oauth2_token(token, requests.Request())
            email = id_info['email']

            # Créer ou récupérer l'utilisateur
            user, created = Utilisateur.objects.get_or_create(email=email, defaults={'username': email})

            # Générer un token JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)"""



class DriverProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils de livreurs
    """
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset
        
        # Filtrage en fonction du rôle de l'utilisateur
        if user.user_type == 'restaurant':
            # Les restaurants voient uniquement leurs livreurs
            queryset = queryset.filter(managed_by_restaurant__owner=user)
        elif user.user_type == 'driver':
            # Les livreurs voient uniquement leur propre profil
            queryset = queryset.filter(user=user)
        elif user.user_type == 'admin':
            # Les admins voient tous les livreurs
            pass
        else:
            # Les clients ne voient pas les livreurs (sauf pour les commandes)
            queryset = queryset.none()
        
        # Filtres via query params
        restaurant_id = self.request.query_params.get('restaurant_id')
        if restaurant_id:
            queryset = queryset.filter(managed_by_restaurant_id=restaurant_id)
        
        is_available = self.request.query_params.get('is_available')
        if is_available is not None:
            queryset = queryset.filter(is_available=is_available.lower() == 'true')
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DriverProfileCreateSerializer
        return DriverProfileSerializer
    
    def perform_create(self, serializer):
        """Créer un livreur géré par le restaurant du user connecté"""
        user = self.request.user
        
        if user.user_type != 'restaurant':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Seuls les restaurants peuvent créer des livreurs")
        
        # Récupérer le restaurant du user
        from apps.restaurants.models import Restaurant
        try:
            restaurant = Restaurant.objects.get(owner=user)
            serializer.save(managed_by_restaurant=restaurant, status='approved')
            logger.info(f"✅ Livreur créé pour le restaurant {restaurant.name}")
        except Restaurant.DoesNotExist:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Vous devez avoir un restaurant pour créer des livreurs")
    
    @action(detail=True, methods=['patch'])
    def update_availability(self, request, pk=None):
        """Mettre à jour la disponibilité du livreur"""
        driver = self.get_object()
        
        # Vérifier que c'est bien le livreur lui-même ou son restaurant
        if request.user != driver.user and (
            not driver.managed_by_restaurant or 
            request.user != driver.managed_by_restaurant.owner
        ):
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        is_available = request.data.get('is_available')
        if is_available is not None:
            driver.is_available = is_available
            driver.save(update_fields=['is_available'])
            
            return Response({
                'status': 'success',
                'is_available': driver.is_available
            })
        
        return Response(
            {'error': 'is_available field required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        """Mettre à jour la position du livreur"""
        driver = self.get_object()
        
        # Seul le livreur peut mettre à jour sa position
        if request.user != driver.user:
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if latitude is not None and longitude is not None:
            driver.current_latitude = latitude
            driver.current_longitude = longitude
            driver.save(update_fields=['current_latitude', 'current_longitude'])
            
            return Response({
                'status': 'success',
                'latitude': driver.current_latitude,
                'longitude': driver.current_longitude
            })
        
        return Response(
            {'error': 'latitude and longitude required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approuver un livreur (pour les restaurants ou admins)"""
        driver = self.get_object()
        
        # Vérifier les permissions
        if request.user.user_type == 'restaurant':
            if not driver.managed_by_restaurant or request.user != driver.managed_by_restaurant.owner:
                return Response(
                    {'error': 'Not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.user_type != 'admin':
            return Response(
                {'error': 'Only restaurants and admins can approve drivers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        driver.status = 'approved'
        driver.save(update_fields=['status'])
        
        logger.info(f"✅ Livreur {driver.user.username} approuvé")
        
        return Response({
            'status': 'success',
            'driver_status': driver.status
        })
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rejeter un livreur"""
        driver = self.get_object()
        
        # Vérifier les permissions
        if request.user.user_type == 'restaurant':
            if not driver.managed_by_restaurant or request.user != driver.managed_by_restaurant.owner:
                return Response(
                    {'error': 'Not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.user_type != 'admin':
            return Response(
                {'error': 'Only restaurants and admins can reject drivers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        driver.status = 'rejected'
        driver.save(update_fields=['status'])
        
        logger.info(f"❌ Livreur {driver.user.username} rejeté")
        
        return Response({
            'status': 'success',
            'driver_status': driver.status
        })
    
    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        """Suspendre un livreur"""
        driver = self.get_object()
        
        # Vérifier les permissions
        if request.user.user_type == 'restaurant':
            if not driver.managed_by_restaurant or request.user != driver.managed_by_restaurant.owner:
                return Response(
                    {'error': 'Not authorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
        elif request.user.user_type != 'admin':
            return Response(
                {'error': 'Only restaurants and admins can suspend drivers'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        driver.status = 'suspended'
        driver.is_available = False
        driver.save(update_fields=['status', 'is_available'])
        
        logger.info(f"⏸️ Livreur {driver.user.username} suspendu")
        
        return Response({
            'status': 'success',
            'driver_status': driver.status
        })
    
    @action(detail=False, methods=['get'])
    def available_drivers(self, request):
        """Obtenir les livreurs disponibles pour une zone"""
        latitude = request.query_params.get('latitude')
        longitude = request.query_params.get('longitude')
        
        queryset = self.get_queryset().filter(
            status='approved',
            is_available=True
        )
        
        # Filtrer par distance si coordonnées fournies
        if latitude and longitude:
            # TODO: Implémenter le filtrage par distance géographique
            # Pour l'instant, on retourne tous les livreurs disponibles
            pass
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Obtenir les statistiques d'un livreur"""
        driver = self.get_object()
        
        # Vérifier les permissions
        if request.user != driver.user and (
            not driver.managed_by_restaurant or 
            request.user != driver.managed_by_restaurant.owner
        ) and request.user.user_type != 'admin':
            return Response(
                {'error': 'Not authorized'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from apps.commandes.models import Order
        from django.db.models import Sum, Avg, Count
        from datetime import timedelta
        from django.utils import timezone
        
        # Statistiques des 30 derniers jours
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        orders = Order.objects.filter(
            driver=driver.user,
            status='delivered',
            created_at__gte=thirty_days_ago
        )
        
        stats = {
            'total_deliveries': driver.total_deliveries,
            'average_rating': driver.average_rating,
            'total_ratings': driver.total_ratings,
            'total_tips': float(driver.total_tips),
            'total_earnings': float(driver.total_earnings),
            
            # Statistiques des 30 derniers jours
            'last_30_days': {
                'deliveries': orders.count(),
                'earnings': float(orders.aggregate(
                    total=Sum('delivery_fee')
                )['total'] or 0),
                'average_delivery_time': None,  # TODO: Calculer si on a les données
            },
            
            # État actuel
            'current_status': driver.status,
            'is_available': driver.is_available,
            'vehicle_type': driver.vehicle_type,
        }
        
        return Response(stats)
