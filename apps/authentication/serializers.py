from rest_framework import serializers
from .models import User
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
