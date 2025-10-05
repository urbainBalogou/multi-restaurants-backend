from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone

from .models import DeliveryTracking, DeliveryZone
from .serializers import (
    DeliveryTrackingSerializer,
    DeliveryTrackingUpdateSerializer,
    DeliveryZoneSerializer
)


class DeliveryTrackingViewSet(viewsets.ModelViewSet):
    queryset = DeliveryTracking.objects.all()
    serializer_class = DeliveryTrackingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return DeliveryTrackingUpdateSerializer
        return DeliveryTrackingSerializer

    @action(detail=True, methods=['post'])
    def update_position(self, request, pk=None):
        """Met à jour la position du livreur"""
        tracking = self.get_object()

        if tracking.driver != request.user:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)

        serializer = DeliveryTrackingUpdateSerializer(tracking, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(last_location_update=timezone.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryZoneViewSet(viewsets.ModelViewSet):
    queryset = DeliveryZone.objects.all()
    serializer_class = DeliveryZoneSerializer
    permission_classes = [IsAuthenticated]
