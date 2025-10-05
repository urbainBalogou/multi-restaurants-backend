from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Order
from .serializers import OrderCreateSerializer, OrderListSerializer, OrderDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Chaque utilisateur ne voit que ses commandes"""
        user = self.request.user
        if user.user_type == 'customer':
            return Order.objects.filter(customer=user)
        elif user.user_type == 'driver':
            return Order.objects.filter(driver=user)
        else:
            return Order.objects.none()

    def get_serializer_class(self):
        """Différencier les serializers selon l’action"""
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Le livreur peut mettre à jour le statut de sa commande"""
        order = self.get_object()
        if request.user.user_type != 'driver' or order.driver != request.user:
            return Response({'error': 'Non autorisé'}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        allowed_statuses = ['picked_up', 'delivered']

        if new_status not in allowed_statuses:
            return Response({'error': 'Statut non autorisé'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        if new_status == 'delivered':
            order.actual_delivery_time = timezone.now()
        order.save()

        return Response({'message': f'Statut mis à jour en {new_status}'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Annulation de la commande par le client"""
        order = self.get_object()
        if (request.user == order.customer and
                order.status in ['pending', 'confirmed']):
            order.status = 'cancelled'
            order.save()
            return Response({'message': 'Commande annulée'})

        return Response(
            {'error': 'Impossible d\'annuler cette commande'},
            status=status.HTTP_400_BAD_REQUEST
        )
