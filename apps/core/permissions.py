from rest_framework import permissions


class IsRestaurantOwnerOrReadOnly(permissions.BasePermission):
    """Permission pour les propriétaires de restaurants"""

    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Écriture seulement pour le propriétaire
        return obj.owner == request.user


class IsOrderOwnerOrRestaurantOrDriver(permissions.BasePermission):
    """Permission pour les commandes - client, restaurant ou livreur"""

    def has_object_permission(self, request, view, obj):
        user = request.user

        return (
                obj.customer == user or  # Le client
                obj.restaurant.owner == user or  # Le propriétaire du restaurant
                obj.driver == user  # Le livreur assigné
        )


class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'restaurant'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
