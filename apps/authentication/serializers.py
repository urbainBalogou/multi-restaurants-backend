from rest_framework import serializers
from .models import User, DriverProfile, CustomerProfile
from django.contrib.auth import authenticate
from django.db import models
import logging
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError


class UtilisateurSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='user_type', read_only=True)
    telephone = serializers.CharField(source='phone_number', read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "telephone", "role", "address", "is_active"]


class LoginSerializer(serializers.Serializer):
    identifiant = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        identifiant = data.get("identifiant")
        password = data.get("password")

        try:
            user = User.objects.get(models.Q(email=identifiant) | models.Q(phone_number=identifiant) |
                                           models.Q(username=identifiant))
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")

        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError("Identifiants incorrects.")

        data['user'] = user
        return data


logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telephone = serializers.CharField(source='phone_number', write_only=True)
    role = serializers.ChoiceField(choices=User.USER_TYPES, source='user_type')

    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'password', 'role']
        extra_kwargs = {
            'role': {'required': True},
            'phone_number': {'required': False}
        }

    def validate_phone_number(self, value):
        """Validation du numéro de téléphone"""
        logger.info(f"🔍 Validation téléphone: {value}")

        if value and User.objects.filter(phone_number=value).exists():
            logger.error(f"❌ Téléphone déjà utilisé: {value}")
            raise serializers.ValidationError("Ce numéro est déjà utilisé.")

        logger.info(f"✅ Téléphone valide: {value}")
        return value

    def validate_email(self, value):
        """Validation de l'email"""
        logger.info(f"🔍 Validation email: {value}")

        if User.objects.filter(email=value).exists():
            logger.error(f"❌ Email déjà utilisé: {value}")
            raise serializers.ValidationError("Cet email est déjà utilisé.")

        logger.info(f"✅ Email valide: {value}")
        return value

    def validate_username(self, value):
        """Validation du nom d'utilisateur"""
        logger.info(f"🔍 Validation username: {value}")

        if User.objects.filter(username=value).exists():
            logger.error(f"❌ Username déjà utilisé: {value}")
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")

        logger.info(f"✅ Username valide: {value}")
        return value

    def validate_password(self, value):
        """Validation du mot de passe"""
        logger.info(f"🔍 Validation password (longueur: {len(value) if value else 0})")

        if not value:
            logger.error("❌ Mot de passe manquant")
            raise serializers.ValidationError("Le mot de passe est requis.")

        if len(value) < 8:
            logger.error(f"❌ Mot de passe trop court: {len(value)} caractères")
            raise serializers.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        logger.info("✅ Mot de passe valide")
        return value

    def validate(self, attrs):
        """Validation globale des données"""
        logger.info(f"🔍 Validation globale des données: {list(attrs.keys())}")

        safe_attrs = {k: v for k, v in attrs.items() if k != 'password'}
        logger.info(f"📋 Données reçues: {safe_attrs}")

        try:
            return super().validate(attrs)
        except ValidationError as e:
            logger.error(f"❌ Erreur de validation globale: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Erreur inattendue lors de la validation: {e}")
            raise ValidationError(f"Erreur de validation: {str(e)}")

    def create(self, validated_data):
        """Création de l'utilisateur"""
        logger.info(f"🔄 Création utilisateur avec données: {list(validated_data.keys())}")

        try:
            password = validated_data.pop('password')
            user = User.objects.create_user(
                **validated_data,
                password=password
            )
            logger.info(f"✅ Utilisateur créé avec succès: {user.email}")
            return user

        except DjangoValidationError as e:
            logger.error(f"❌ Erreur de validation Django: {e}")
            raise ValidationError(f"Erreur de validation: {e}")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la création: {e}")
            raise ValidationError(f"Erreur de création: {str(e)}")


class UserSerializer(serializers.ModelSerializer):
    """Serializer standard pour User"""
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'address', 'latitude', 'longitude',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class DriverProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil des livreurs"""
    user = UserSerializer(read_only=True)
    restaurant_name = serializers.CharField(source='managed_by_restaurant.name', read_only=True, allow_null=True)
    is_independent = serializers.BooleanField(read_only=True)

    class Meta:
        model = DriverProfile
        fields = [
            'id', 'user', 'managed_by_restaurant', 'restaurant_name',
            'vehicle_type', 'license_plate', 'status', 'is_available',
            'current_latitude', 'current_longitude',
            'driver_license_number', 'driver_license_photo', 'id_card_photo',
            'vehicle_insurance', 'average_rating', 'total_ratings',
            'total_deliveries', 'total_tips', 'total_earnings',
            'max_delivery_distance_km', 'preferred_zones', 'availability_schedule',
            'is_independent'
        ]
        read_only_fields = [
            'average_rating', 'total_ratings', 'total_deliveries',
            'total_tips', 'total_earnings'
        ]


class DriverProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer pour créer un profil de livreur"""
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = DriverProfile
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'managed_by_restaurant', 'vehicle_type',
            'license_plate', 'driver_license_number', 'driver_license_photo',
            'id_card_photo', 'vehicle_insurance', 'max_delivery_distance_km',
            'preferred_zones', 'availability_schedule'
        ]

    def create(self, validated_data):
        # Extraire les données utilisateur
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name', ''),
            'last_name': validated_data.pop('last_name', ''),
            'phone_number': validated_data.pop('phone_number'),
            'user_type': 'driver',
        }

        # Créer l'utilisateur
        password = user_data.pop('password')
        user = User.objects.create_user(**user_data, password=password)

        # Créer le profil livreur
        driver_profile = DriverProfile.objects.create(user=user, **validated_data)

        logger.info(f"✅ Livreur créé: {user.username} (Restaurant: {driver_profile.managed_by_restaurant})")

        return driver_profile


class CustomerProfileSerializer(serializers.ModelSerializer):
    """Serializer pour le profil des clients"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'delivery_addresses', 'favorite_restaurants']
