from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
from apps.authentication.models import DriverProfile
from geopy.distance import geodesic


@shared_task
def send_order_notification(order_id, notification_type):
    """Envoie des notifications pour les commandes"""
    try:
        order = Order.objects.get(id=order_id)

        if notification_type == 'new_order':
            # Notifier le restaurant
            subject = f"Nouvelle commande #{order.order_number}"
            message = f"Vous avez reçu une nouvelle commande de {order.customer.username}"
            recipient = order.restaurant.owner.email

        elif notification_type == 'ready_for_pickup':
            # Notifier le livreur
            subject = f"Commande prête #{order.order_number}"
            message = f"La commande est prête à être récupérée chez {order.restaurant.name}"
            recipient = order.driver.email

        if recipient:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )

    except Order.DoesNotExist:
        pass


@shared_task
def assign_driver(order_id):
    """Assigne automatiquement un livreur à une commande"""
    try:
        order = Order.objects.get(id=order_id)

        # Trouver les livreurs disponibles dans un rayon de 5km
        restaurant_location = (order.restaurant.latitude, order.restaurant.longitude)

        available_drivers = DriverProfile.objects.filter(
            is_available=True,
            current_latitude__isnull=False,
            current_longitude__isnull=False
        ).select_related('user')

        closest_driver = None
        min_distance = float('inf')

        for driver_profile in available_drivers:
            driver_location = (driver_profile.current_latitude, driver_profile.current_longitude)
            distance = geodesic(restaurant_location, driver_location).kilometers

            if distance < min_distance and distance <= 5:  # Dans un rayon de 5km
                min_distance = distance
                closest_driver = driver_profile.user

        if closest_driver:
            order.driver = closest_driver
            order.save()

            # Marquer le livreur comme non disponible
            closest_driver.driver_profile.is_available = False
            closest_driver.driver_profile.save()

            # Notifier le livreur
            send_order_notification.delay(order.id, 'assigned')

    except Order.DoesNotExist:
        pass
