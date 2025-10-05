from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import User


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
        global Utilisateur
        print("🔄 DÉBUT PROCESSUS D'INSCRIPTION")
        print("=" * 50)

        # Log des données reçues (masquer le mot de passe pour la sécurité)
        safe_data = {k: v for k, v in request.data.items() if k not in ['password', 'password_confirmation']}
        print(f"📋 Données reçues (safe): {safe_data}")
        print(f"🔑 Mot de passe fourni: {'Oui' if request.data.get('password') else 'Non'}")
        print(f"📊 Nombre total de champs: {len(request.data)}")

        # Vérification des champs requis
        required_fields = ['username', 'email', 'password', 'role']
        missing_fields = [field for field in required_fields if field not in request.data]
        if missing_fields:
            print(f"⚠️ Champs requis manquants: {missing_fields}")

        # Création du serializer
        serializer = RegisterSerializer(data=request.data)

        print("\n🔍 PHASE DE VALIDATION")
        print("-" * 30)

        # Validation SANS lever d'exception pour voir les erreurs
        if serializer.is_valid():
            print("✅ Validation réussie - Procédure de création...")

            try:
                # Création de l'utilisateur
                user = serializer.save()
                print(f"✅ Utilisateur créé avec succès: {user.email} (ID: {user.id})")
                refresh = RefreshToken.for_user(user)
                user_data = UtilisateurSerializer(user).data
                user_data['api_token'] = str(refresh.access_token)

                return Response({
                    "message": "Inscription réussie",
                    "data": user_data
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                print(f"❌ Erreur lors de la création de l'utilisateur: {e}")
                print(f"🔍 Type d'erreur: {type(e).__name__}")

                return Response({
                    "message": "Erreur lors de la création de l'utilisateur",
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            for field, errors in serializer.errors.items():
                print(f"❌ Champ '{field}':")
                for error in errors:
                    print(f"   → {error}")

                received_value = request.data.get(field, 'NON_FOURNI')
                print(f"   📝 Valeur reçue: {received_value}")
                print(f"   📊 Type: {type(received_value).__name__}")

                # Vérifications supplémentaires selon le champ
                if field == 'email' and received_value != 'NON_FOURNI':
                    from .models import Utilisateur  # Ajustez l'import selon votre structure
                    exists = Utilisateur.objects.filter(email=received_value).exists()
                    print(f"   🔍 Email existe déjà en DB: {exists}")

                elif field == 'telephone' and received_value != 'NON_FOURNI':
                    exists = Utilisateur.objects.filter(telephone=received_value).exists()
                    print(f"   🔍 Téléphone existe déjà en DB: {exists}")

                elif field == 'username' and received_value != 'NON_FOURNI':
                    exists = Utilisateur.objects.filter(username=received_value).exists()
                    print(f"   🔍 Username existe déjà en DB: {exists}")

                elif field == 'password' and received_value != 'NON_FOURNI':
                    print(f"   🔍 Longueur mot de passe: {len(str(received_value))}")

                print()  # Ligne vide pour la lisibilité

            # Retourner les erreurs détaillées
            return Response({
                "message": "Erreurs de validation",
                "errors": serializer.errors,
                "debug_info": {
                    "received_fields": list(request.data.keys()),
                    "missing_required": missing_fields,
                    "total_errors": len(serializer.errors)
                }
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


