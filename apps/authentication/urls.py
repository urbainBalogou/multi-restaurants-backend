from django.urls import path, include
from .views import LoginAPIView, RegisterAPIView, UtilisateurViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UtilisateurViewSet, basename='utilisateur')


urlpatterns = [
    path("", include(router.urls)),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
]
