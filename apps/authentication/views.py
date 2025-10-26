from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from .models import User
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


