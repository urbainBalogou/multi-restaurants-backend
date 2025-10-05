from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_order_notification, assign_driver


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    """Actions automatiques après sauvegarde d'une commande"""

    if created:
        # Nouvelle commande - notifier le restaurant
        send_order_notification.delay(instance.id, 'new_order')

    elif instance.status == 'confirmed':
        # Commande confirmée - chercher un livreur
        assign_driver.delay(instance.id)

    elif instance.status == 'ready':
        # Commande prête - notifier le livreur
        if instance.driver:
            send_order_notification.delay(instance.id, 'ready_for_pickup')