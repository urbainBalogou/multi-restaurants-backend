from geopy.distance import geodesic
import json

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calcule la distance entre deux points GPS"""
    try:
        point1 = (float(lat1), float(lng1))
        point2 = (float(lat2), float(lng2))
        return geodesic(point1, point2).kilometers
    except (ValueError, TypeError):
        return None


def calculate_delivery_fee(distance_km, base_fee=2.5, per_km_rate=0.5):
    """Calcule les frais de livraison selon la distance"""
    if distance_km <= 2:
        return base_fee
    return base_fee + ((distance_km - 2) * per_km_rate)


def estimate_delivery_time(distance_km, preparation_time=20):
    """Estime le temps de livraison total"""
    # Vitesse moyenne: 30km/h
    travel_time = (distance_km / 30) * 60  # en minutes
    return preparation_time + int(travel_time)


def format_opening_hours():
    """Format standard pour les horaires d'ouverture"""
    return {
        "monday": {"open": "09:00", "close": "22:00", "is_open": True},
        "tuesday": {"open": "09:00", "close": "22:00", "is_open": True},
        "wednesday": {"open": "09:00", "close": "22:00", "is_open": True},
        "thursday": {"open": "09:00", "close": "22:00", "is_open": True},
        "friday": {"open": "09:00", "close": "23:00", "is_open": True},
        "saturday": {"open": "10:00", "close": "23:00", "is_open": True},
        "sunday": {"open": "10:00", "close": "21:00", "is_open": True}
    }