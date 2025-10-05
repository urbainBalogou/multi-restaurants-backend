from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryTrackingViewSet, DeliveryZoneViewSet

router = DefaultRouter()
router.register(r'tracking', DeliveryTrackingViewSet, basename='tracking')
router.register(r'delivery-zones', DeliveryZoneViewSet, basename='delivery-zone')

urlpatterns = [
    path('', include(router.urls)),
]
