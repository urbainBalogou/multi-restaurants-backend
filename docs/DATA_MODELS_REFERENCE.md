# Référence des modèles de données - Multi-Restaurants API

## Table des matières
1. [Authentication Models](#authentication-models)
2. [Restaurant Models](#restaurant-models)
3. [Order Models](#order-models)
4. [Delivery Models](#delivery-models)
5. [Promotion Models](#promotion-models)
6. [Relations entre modèles](#relations-entre-modèles)
7. [Formats JSON spécifiques](#formats-json-spécifiques)
8. [États et workflows](#états-et-workflows)

---

## Authentication Models

### User

Modèle utilisateur principal qui hérite de `AbstractUser` Django.

**Table** : `authentication_user`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `username` | String | ✓ | - | Nom d'utilisateur unique |
| `email` | Email | ✓ | - | Email unique |
| `password` | String | ✓ | - | Mot de passe hashé |
| `first_name` | String | ✗ | '' | Prénom |
| `last_name` | String | ✗ | '' | Nom |
| `user_type` | String | ✓ | 'customer' | Type d'utilisateur |
| `phone_number` | PhoneNumber | ✗ | null | Numéro de téléphone |
| `address` | Text | ✗ | '' | Adresse complète |
| `latitude` | Float | ✗ | null | Latitude GPS |
| `longitude` | Float | ✗ | null | Longitude GPS |
| `is_active` | Boolean | ✓ | true | Compte actif |
| `is_staff` | Boolean | ✓ | false | Accès admin |
| `is_superuser` | Boolean | ✓ | false | Super admin |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |
| `last_login` | DateTime | ✗ | null | Dernière connexion |

**Choix `user_type`** :
```python
{
    'customer': 'Client',
    'restaurant': 'Restaurant',
    'driver': 'Livreur',
    'admin': 'Administrateur'
}
```

**Exemple JSON (Response)** :
```json
{
  "id": 1,
  "username": "john.doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "customer",
  "phone_number": "+33612345678",
  "address": "123 Rue de la Paix, 75001 Paris",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T14:22:00Z"
}
```

---

### CustomerProfile

Profil complémentaire pour les clients.

**Table** : `authentication_customerprofile`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `user` | ForeignKey(User) | ✓ | - | Lien vers User |
| `delivery_addresses` | JSON | ✗ | [] | Liste d'adresses |
| `favorite_restaurants` | ManyToMany | ✗ | [] | Restaurants favoris |

**Format `delivery_addresses`** :
```json
[
  {
    "id": "home",
    "label": "Maison",
    "address": "123 Rue de la Paix, 75001 Paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "instructions": "Digicode : 1234A",
    "is_default": true
  },
  {
    "id": "work",
    "label": "Bureau",
    "address": "456 Avenue des Champs-Élysées, 75008 Paris",
    "latitude": 48.8698,
    "longitude": 2.3078,
    "instructions": "Bâtiment B, 3ème étage",
    "is_default": false
  }
]
```

---

### DriverProfile

Profil complémentaire pour les livreurs.

**Table** : `authentication_driverprofile`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `user` | ForeignKey(User) | ✓ | - | Lien vers User |
| `vehicle_type` | String | ✓ | - | Type de véhicule |
| `license_plate` | String | ✓ | - | Plaque d'immatriculation |
| `is_available` | Boolean | ✓ | false | Disponible pour livrer |
| `current_latitude` | Float | ✗ | null | Position actuelle (lat) |
| `current_longitude` | Float | ✗ | null | Position actuelle (lon) |
| `average_rating` | Float | ✓ | 0.0 | Note moyenne (0-5) |
| `total_ratings` | Integer | ✓ | 0 | Nombre d'évaluations |
| `total_deliveries` | Integer | ✓ | 0 | Nombre de livraisons |
| `total_tips` | Decimal | ✓ | 0.00 | Total des pourboires |

**Choix `vehicle_type`** :
```python
{
    'bike': 'Vélo',
    'scooter': 'Scooter',
    'car': 'Voiture'
}
```

**Exemple JSON (Response)** :
```json
{
  "id": 5,
  "user": {
    "id": 25,
    "username": "driver.martin",
    "first_name": "Pierre",
    "last_name": "Martin",
    "phone_number": "+33698765432"
  },
  "vehicle_type": "scooter",
  "license_plate": "AB-123-CD",
  "is_available": true,
  "current_latitude": 48.8606,
  "current_longitude": 2.3376,
  "average_rating": 4.7,
  "total_ratings": 156,
  "total_deliveries": 423,
  "total_tips": 287.50
}
```

---

## Restaurant Models

### Restaurant

Modèle principal pour les restaurants.

**Table** : `restaurants_restaurant`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `owner` | ForeignKey(User) | ✓ | - | Propriétaire du restaurant |
| `name` | String(200) | ✓ | - | Nom du restaurant |
| `description` | Text | ✗ | '' | Description |
| `image` | ImageField | ✗ | null | Image principale |
| `address` | Text | ✓ | - | Adresse complète |
| `latitude` | Float | ✓ | - | Latitude GPS |
| `longitude` | Float | ✓ | - | Longitude GPS |
| `phone_number` | PhoneNumber | ✓ | - | Téléphone |
| `email` | Email | ✗ | '' | Email |
| `opening_hours` | JSON | ✓ | {} | Horaires d'ouverture |
| `is_active` | Boolean | ✓ | true | Restaurant actif |
| `is_accepting_orders` | Boolean | ✓ | true | Accepte les commandes |
| `average_rating` | Float | ✓ | 0.0 | Note moyenne (0-5) |
| `total_reviews` | Integer | ✓ | 0 | Nombre d'avis |
| `delivery_fee` | Decimal | ✓ | 0.00 | Frais de livraison (€) |
| `free_delivery_threshold` | Decimal | ✓ | 0.00 | Seuil livraison gratuite (€) |
| `delivery_radius_km` | Float | ✓ | 5.0 | Rayon de livraison (km) |
| `estimated_delivery_time` | Integer | ✓ | 30 | Temps estimé (minutes) |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Format `opening_hours`** :
```json
{
  "monday": {"open": "11:00", "close": "22:00", "is_closed": false},
  "tuesday": {"open": "11:00", "close": "22:00", "is_closed": false},
  "wednesday": {"open": "11:00", "close": "22:00", "is_closed": false},
  "thursday": {"open": "11:00", "close": "23:00", "is_closed": false},
  "friday": {"open": "11:00", "close": "00:00", "is_closed": false},
  "saturday": {"open": "12:00", "close": "00:00", "is_closed": false},
  "sunday": {"open": "12:00", "close": "22:00", "is_closed": false}
}
```

**Exemple JSON (Response)** :
```json
{
  "id": 12,
  "name": "Burger King",
  "description": "Fast food américain de qualité",
  "image": "https://api.example.com/media/restaurants/burger-king.jpg",
  "address": "10 Boulevard Saint-Michel, 75006 Paris",
  "latitude": 48.8534,
  "longitude": 2.3442,
  "phone_number": "+33140123456",
  "email": "contact@burgerking-paris.fr",
  "opening_hours": {
    "monday": {"open": "11:00", "close": "22:00", "is_closed": false},
    "tuesday": {"open": "11:00", "close": "22:00", "is_closed": false}
  },
  "is_active": true,
  "is_accepting_orders": true,
  "average_rating": 4.3,
  "total_reviews": 234,
  "delivery_fee": 2.99,
  "free_delivery_threshold": 25.00,
  "delivery_radius_km": 5.0,
  "estimated_delivery_time": 30,
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-02-15T10:30:00Z"
}
```

---

### Category

Catégories de plats/restaurants.

**Table** : `restaurants_category`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `name` | String(100) | ✓ | - | Nom de la catégorie |
| `description` | Text | ✗ | '' | Description |
| `image` | ImageField | ✗ | null | Image de la catégorie |
| `is_active` | Boolean | ✓ | true | Catégorie active |
| `order` | Integer | ✓ | 0 | Ordre d'affichage |

**Exemple JSON (Response)** :
```json
{
  "id": 5,
  "name": "Burgers",
  "description": "Burgers et sandwichs",
  "image": "https://api.example.com/media/categories/burgers.jpg",
  "is_active": true,
  "order": 1
}
```

---

### MenuItem

Articles du menu des restaurants.

**Table** : `restaurants_menuitem`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `restaurant` | ForeignKey(Restaurant) | ✓ | - | Restaurant parent |
| `category` | ForeignKey(Category) | ✗ | null | Catégorie du plat |
| `name` | String(200) | ✓ | - | Nom du plat |
| `description` | Text | ✗ | '' | Description |
| `price` | Decimal | ✓ | - | Prix (€) |
| `image` | ImageField | ✗ | null | Image du plat |
| `is_available` | Boolean | ✓ | true | Disponible |
| `preparation_time` | Integer | ✓ | 15 | Temps de préparation (min) |
| `has_options` | Boolean | ✓ | false | A des options |
| `options` | JSON | ✗ | {} | Options de personnalisation |
| `calories` | Integer | ✗ | null | Calories |
| `allergens` | JSON | ✗ | [] | Allergènes |
| `order_count` | Integer | ✓ | 0 | Nombre de commandes |
| `average_rating` | Float | ✓ | 0.0 | Note moyenne |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Format `options`** :
```json
{
  "size": {
    "label": "Taille",
    "required": true,
    "choices": [
      {"value": "small", "label": "Petit", "price_modifier": 0.00},
      {"value": "medium", "label": "Moyen", "price_modifier": 1.50},
      {"value": "large", "label": "Grand", "price_modifier": 2.50}
    ]
  },
  "extras": {
    "label": "Suppléments",
    "required": false,
    "multiple": true,
    "choices": [
      {"value": "cheese", "label": "Fromage supplémentaire", "price_modifier": 1.00},
      {"value": "bacon", "label": "Bacon", "price_modifier": 1.50},
      {"value": "avocado", "label": "Avocat", "price_modifier": 2.00}
    ]
  },
  "sauce": {
    "label": "Sauce",
    "required": false,
    "choices": [
      {"value": "ketchup", "label": "Ketchup", "price_modifier": 0.00},
      {"value": "mayo", "label": "Mayonnaise", "price_modifier": 0.00},
      {"value": "bbq", "label": "BBQ", "price_modifier": 0.50}
    ]
  }
}
```

**Format `allergens`** :
```json
["gluten", "dairy", "nuts", "eggs"]
```

**Exemple JSON (Response)** :
```json
{
  "id": 45,
  "restaurant_id": 12,
  "category": {
    "id": 5,
    "name": "Burgers"
  },
  "name": "Burger Royal",
  "description": "Burger avec steak haché, fromage, salade, tomate, oignons",
  "price": 8.90,
  "image": "https://api.example.com/media/menu_items/burger-royal.jpg",
  "is_available": true,
  "preparation_time": 15,
  "has_options": true,
  "options": {
    "size": {...},
    "extras": {...}
  },
  "calories": 650,
  "allergens": ["gluten", "dairy"],
  "order_count": 1234,
  "average_rating": 4.6,
  "created_at": "2024-01-10T08:00:00Z",
  "updated_at": "2024-02-10T12:00:00Z"
}
```

---

### RestaurantReview

Avis sur les restaurants.

**Table** : `restaurants_restaurantreview`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `restaurant` | ForeignKey(Restaurant) | ✓ | - | Restaurant évalué |
| `customer` | ForeignKey(User) | ✓ | - | Client auteur |
| `rating` | Integer | ✓ | - | Note (1-5) |
| `comment` | Text | ✗ | '' | Commentaire |
| `created_at` | DateTime | Auto | now | Date de création |

**Contrainte** : Un client ne peut laisser qu'un seul avis par restaurant (unique together).

**Exemple JSON (Response)** :
```json
{
  "id": 123,
  "restaurant_id": 12,
  "customer": {
    "id": 45,
    "username": "marie.dupont",
    "first_name": "Marie",
    "last_name": "Dupont"
  },
  "rating": 5,
  "comment": "Excellent restaurant, service rapide et plats délicieux !",
  "created_at": "2024-02-10T19:30:00Z"
}
```

---

## Order Models

### Order

Commandes passées par les clients.

**Table** : `commandes_order`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | UUID | Auto | uuid4 | ID unique UUID |
| `order_number` | String(20) | Auto | - | Numéro de commande |
| `customer` | ForeignKey(User) | ✓ | - | Client |
| `restaurant` | ForeignKey(Restaurant) | ✓ | - | Restaurant |
| `driver` | ForeignKey(User) | ✗ | null | Livreur assigné |
| `status` | String(20) | ✓ | 'pending' | Statut de la commande |
| `estimated_delivery_time` | DateTime | ✗ | null | Heure estimée de livraison |
| `actual_delivery_time` | DateTime | ✗ | null | Heure réelle de livraison |
| `subtotal` | Decimal | ✓ | - | Sous-total (€) |
| `delivery_fee` | Decimal | ✓ | 0.00 | Frais de livraison (€) |
| `tax` | Decimal | ✓ | 0.00 | Taxes (€) |
| `total_amount` | Decimal | ✓ | - | Montant total (€) |
| `payment_method` | String(20) | ✓ | - | Méthode de paiement |
| `payment_status` | String(20) | ✓ | 'pending' | Statut du paiement |
| `delivery_address` | JSON | ✓ | - | Adresse de livraison |
| `delivery_latitude` | Float | ✓ | - | Latitude de livraison |
| `delivery_longitude` | Float | ✓ | - | Longitude de livraison |
| `customer_notes` | Text | ✗ | '' | Notes du client |
| `restaurant_notes` | Text | ✗ | '' | Notes du restaurant |
| `driver_notes` | Text | ✗ | '' | Notes du livreur |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Choix `status`** :
```python
{
    'pending': 'En attente',
    'confirmed': 'Confirmée',
    'preparing': 'En préparation',
    'ready': 'Prête',
    'picked_up': 'Récupérée',
    'delivered': 'Livrée',
    'cancelled': 'Annulée'
}
```

**Choix `payment_method`** :
```python
{
    'cash': 'Espèces',
    'card': 'Carte',
    'mobile': 'Paiement mobile'
}
```

**Format `delivery_address`** :
```json
{
  "label": "Maison",
  "address": "123 Rue de la Paix, 75001 Paris",
  "building": "Bâtiment A",
  "floor": "3ème étage",
  "apartment": "Appartement 12",
  "instructions": "Digicode : 1234A, Interphone : DUPONT",
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

**Exemple JSON (Response)** :
```json
{
  "id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "order_number": "12345678",
  "customer": {
    "id": 45,
    "username": "marie.dupont",
    "first_name": "Marie",
    "last_name": "Dupont",
    "phone_number": "+33612345678"
  },
  "restaurant": {
    "id": 12,
    "name": "Burger King",
    "phone_number": "+33140123456"
  },
  "driver": {
    "id": 25,
    "username": "driver.martin",
    "first_name": "Pierre",
    "last_name": "Martin",
    "phone_number": "+33698765432"
  },
  "status": "delivering",
  "estimated_delivery_time": "2024-02-15T19:30:00Z",
  "actual_delivery_time": null,
  "subtotal": 24.80,
  "delivery_fee": 2.99,
  "tax": 0.00,
  "total_amount": 27.79,
  "payment_method": "card",
  "payment_status": "paid",
  "delivery_address": {
    "label": "Maison",
    "address": "123 Rue de la Paix, 75001 Paris",
    "instructions": "Digicode : 1234A"
  },
  "delivery_latitude": 48.8566,
  "delivery_longitude": 2.3522,
  "customer_notes": "Pas d'oignons svp",
  "restaurant_notes": "",
  "driver_notes": "",
  "items": [
    {
      "id": 1,
      "menu_item": {
        "id": 45,
        "name": "Burger Royal",
        "image": "https://api.example.com/media/menu_items/burger-royal.jpg"
      },
      "quantity": 2,
      "unit_price": 8.90,
      "total_price": 17.80,
      "selected_options": {
        "size": "medium",
        "extras": ["cheese", "bacon"]
      },
      "special_instructions": "Bien cuit"
    },
    {
      "id": 2,
      "menu_item": {
        "id": 52,
        "name": "Frites",
        "image": "https://api.example.com/media/menu_items/frites.jpg"
      },
      "quantity": 1,
      "unit_price": 3.50,
      "total_price": 3.50,
      "selected_options": {},
      "special_instructions": ""
    }
  ],
  "created_at": "2024-02-15T18:45:00Z",
  "updated_at": "2024-02-15T19:10:00Z"
}
```

---

### OrderItem

Articles d'une commande.

**Table** : `commandes_orderitem`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `order` | ForeignKey(Order) | ✓ | - | Commande parent |
| `menu_item` | ForeignKey(MenuItem) | ✓ | - | Article du menu |
| `quantity` | Integer | ✓ | 1 | Quantité |
| `unit_price` | Decimal | ✓ | - | Prix unitaire (€) |
| `total_price` | Decimal | Auto | - | Prix total (€) |
| `selected_options` | JSON | ✗ | {} | Options sélectionnées |
| `special_instructions` | Text | ✗ | '' | Instructions spéciales |

**Format `selected_options`** :
```json
{
  "size": "medium",
  "extras": ["cheese", "bacon"],
  "sauce": "bbq"
}
```

---

## Delivery Models

### DeliveryTracking

Suivi en temps réel des livraisons.

**Table** : `livraison_deliverytracking`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `order` | OneToOneField(Order) | ✓ | - | Commande |
| `driver` | ForeignKey(User) | ✓ | - | Livreur |
| `current_latitude` | Float | ✗ | null | Position actuelle (lat) |
| `current_longitude` | Float | ✗ | null | Position actuelle (lon) |
| `last_location_update` | DateTime | ✗ | null | Dernière maj position |
| `estimated_arrival` | DateTime | ✗ | null | Heure d'arrivée estimée |
| `distance_remaining_km` | Float | ✗ | null | Distance restante (km) |
| `picked_up_at` | DateTime | ✗ | null | Heure de récupération |
| `delivered_at` | DateTime | ✗ | null | Heure de livraison |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Exemple JSON (Response)** :
```json
{
  "id": 789,
  "order_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "driver": {
    "id": 25,
    "first_name": "Pierre",
    "last_name": "Martin",
    "phone_number": "+33698765432",
    "vehicle_type": "scooter"
  },
  "current_latitude": 48.8580,
  "current_longitude": 2.3410,
  "last_location_update": "2024-02-15T19:15:00Z",
  "estimated_arrival": "2024-02-15T19:30:00Z",
  "distance_remaining_km": 1.2,
  "picked_up_at": "2024-02-15T19:05:00Z",
  "delivered_at": null
}
```

---

### DeliveryZone

Zones de livraison des restaurants.

**Table** : `livraison_deliveryzone`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `name` | String(100) | ✓ | - | Nom de la zone |
| `restaurant` | ForeignKey(Restaurant) | ✓ | - | Restaurant |
| `coordinates` | JSON | ✓ | - | Polygone de la zone |
| `delivery_fee` | Decimal | ✓ | - | Frais de livraison (€) |
| `estimated_time` | Integer | ✓ | - | Temps estimé (minutes) |
| `is_active` | Boolean | ✓ | true | Zone active |

**Format `coordinates`** (GeoJSON Polygon) :
```json
{
  "type": "Polygon",
  "coordinates": [
    [
      [2.3522, 48.8566],
      [2.3600, 48.8566],
      [2.3600, 48.8600],
      [2.3522, 48.8600],
      [2.3522, 48.8566]
    ]
  ]
}
```

---

### DriverRating

Évaluations des livreurs par les clients.

**Table** : `livraison_driverrating`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `order` | OneToOneField(Order) | ✓ | - | Commande |
| `driver` | ForeignKey(User) | ✓ | - | Livreur évalué |
| `customer` | ForeignKey(User) | ✓ | - | Client auteur |
| `overall_rating` | Integer | ✓ | - | Note globale (1-5) |
| `punctuality_rating` | Integer | ✗ | null | Ponctualité (1-5) |
| `professionalism_rating` | Integer | ✗ | null | Professionnalisme (1-5) |
| `care_rating` | Integer | ✗ | null | Soin (1-5) |
| `comment` | Text | ✗ | '' | Commentaire |
| `tip_amount` | Decimal | ✓ | 0.00 | Pourboire (€) |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Exemple JSON (Request - Create)** :
```json
{
  "order_id": "a1b2c3d4-e5f6-4a5b-8c9d-0e1f2a3b4c5d",
  "overall_rating": 5,
  "punctuality_rating": 5,
  "professionalism_rating": 5,
  "care_rating": 4,
  "comment": "Livraison rapide et livreur très sympa !",
  "tip_amount": 2.00
}
```

---

## Promotion Models

### Coupon

Codes promo utilisables par les clients.

**Table** : `promotions_coupon`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `code` | String(50) | ✓ | - | Code promo unique |
| `description` | Text | ✗ | '' | Description |
| `discount_type` | String(20) | ✓ | - | Type de réduction |
| `discount_value` | Decimal | ✓ | - | Valeur de la réduction |
| `min_order_amount` | Decimal | ✓ | 0 | Montant minimum (€) |
| `max_discount_amount` | Decimal | ✗ | null | Réduction max (€) |
| `valid_from` | DateTime | ✓ | - | Date de début |
| `valid_until` | DateTime | ✓ | - | Date de fin |
| `is_active` | Boolean | ✓ | true | Coupon actif |
| `usage_limit` | Integer | ✗ | null | Limite totale |
| `usage_limit_per_user` | Integer | ✓ | 1 | Limite par utilisateur |
| `usage_count` | Integer | ✓ | 0 | Nombre d'utilisations |
| `applicable_restaurants` | ManyToMany | ✗ | [] | Restaurants applicables |
| `allowed_users` | ManyToMany | ✗ | [] | Utilisateurs autorisés |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Choix `discount_type`** :
```python
{
    'percentage': 'Pourcentage',
    'fixed': 'Montant fixe',
    'free_delivery': 'Livraison gratuite'
}
```

**Exemple JSON (Response)** :
```json
{
  "id": 15,
  "code": "WELCOME10",
  "description": "10% de réduction pour les nouveaux clients",
  "discount_type": "percentage",
  "discount_value": 10.00,
  "min_order_amount": 15.00,
  "max_discount_amount": 5.00,
  "valid_from": "2024-01-01T00:00:00Z",
  "valid_until": "2024-12-31T23:59:59Z",
  "is_active": true,
  "usage_limit": 1000,
  "usage_limit_per_user": 1,
  "usage_count": 234,
  "applicable_restaurants": [],
  "can_use": true,
  "times_used_by_user": 0
}
```

---

### CouponUsage

Historique d'utilisation des coupons.

**Table** : `promotions_couponusage`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `coupon` | ForeignKey(Coupon) | ✓ | - | Coupon utilisé |
| `user` | ForeignKey(User) | ✓ | - | Utilisateur |
| `order` | ForeignKey(Order) | ✓ | - | Commande |
| `discount_amount` | Decimal | ✓ | - | Montant de la réduction (€) |
| `used_at` | DateTime | Auto | now | Date d'utilisation |

---

### Promotion

Promotions temporaires sur des articles (gérées par les restaurants).

**Table** : `promotions_promotion`

| Champ | Type | Requis | Default | Description |
|-------|------|--------|---------|-------------|
| `id` | Integer | Auto | Auto-increment | ID unique |
| `restaurant` | ForeignKey(Restaurant) | ✓ | - | Restaurant |
| `name` | String(200) | ✓ | - | Nom de la promotion |
| `description` | Text | ✗ | '' | Description |
| `promotion_type` | String(20) | ✓ | - | Type de promotion |
| `discount_value` | Decimal | ✓ | - | Valeur de la réduction |
| `buy_quantity` | Integer | ✗ | null | Quantité à acheter |
| `get_quantity` | Integer | ✗ | null | Quantité gratuite |
| `applicable_items` | ManyToMany | ✗ | [] | Articles concernés |
| `valid_from` | DateTime | ✓ | - | Date de début |
| `valid_until` | DateTime | ✓ | - | Date de fin |
| `is_active` | Boolean | ✓ | true | Promotion active |
| `applicable_days` | JSON | ✗ | [] | Jours applicables |
| `start_time` | Time | ✗ | null | Heure de début |
| `end_time` | Time | ✗ | null | Heure de fin |
| `priority` | Integer | ✓ | 0 | Priorité |
| `image` | ImageField | ✗ | null | Image promo |
| `created_at` | DateTime | Auto | now | Date de création |
| `updated_at` | DateTime | Auto | now | Date de modification |

**Choix `promotion_type`** :
```python
{
    'percentage': 'Pourcentage',
    'fixed': 'Montant fixe',
    'buy_x_get_y': 'Achetez X obtenez Y'
}
```

**Format `applicable_days`** :
```json
[0, 1, 2, 3, 4, 5, 6]
```
Où 0 = Lundi, 1 = Mardi, ..., 6 = Dimanche

**Exemple JSON (Response)** :
```json
{
  "id": 8,
  "restaurant_id": 12,
  "name": "Happy Hour",
  "description": "20% de réduction sur tous les burgers",
  "promotion_type": "percentage",
  "discount_value": 20.00,
  "buy_quantity": null,
  "get_quantity": null,
  "applicable_items": [45, 46, 47],
  "valid_from": "2024-02-01T00:00:00Z",
  "valid_until": "2024-02-28T23:59:59Z",
  "is_active": true,
  "applicable_days": [0, 1, 2, 3, 4],
  "start_time": "17:00:00",
  "end_time": "19:00:00",
  "priority": 10,
  "image": "https://api.example.com/media/promotions/happy-hour.jpg",
  "is_valid_now": true
}
```

---

## Relations entre modèles

### Diagramme des relations

```
User (customer) ──┬─── CustomerProfile
                  │         └─── favorite_restaurants (ManyToMany) ─── Restaurant
                  │
                  ├─── Order (as customer)
                  │         ├─── restaurant (ForeignKey) ─── Restaurant
                  │         ├─── driver (ForeignKey) ─── User (driver)
                  │         ├─── items (OneToMany) ─── OrderItem
                  │         │         └─── menu_item (ForeignKey) ─── MenuItem
                  │         ├─── tracking (OneToOne) ─── DeliveryTracking
                  │         ├─── driver_rating (OneToOne) ─── DriverRating
                  │         └─── coupon_usage (OneToMany) ─── CouponUsage
                  │
                  ├─── RestaurantReview (as customer)
                  │
                  └─── CouponUsage (as user)

User (driver) ─── DriverProfile
                  ├─── Order (as driver)
                  ├─── DeliveryTracking
                  └─── DriverRating (as driver)

User (restaurant) ─── Restaurant (as owner)
                         ├─── MenuItem
                         │         └─── category (ForeignKey) ─── Category
                         ├─── RestaurantReview
                         ├─── DeliveryZone
                         ├─── Promotion
                         │         └─── applicable_items (ManyToMany) ─── MenuItem
                         └─── Coupon (applicable_restaurants)

Coupon ─── CouponUsage
           └─── order (ForeignKey) ─── Order
```

---

## Formats JSON spécifiques

### Adresse de livraison complète
```json
{
  "id": "home",
  "label": "Maison",
  "address": "123 Rue de la Paix, 75001 Paris",
  "street_number": "123",
  "street_name": "Rue de la Paix",
  "city": "Paris",
  "postal_code": "75001",
  "country": "France",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "building": "Bâtiment A",
  "floor": "3ème étage",
  "apartment": "12",
  "instructions": "Digicode : 1234A, Interphone : DUPONT",
  "is_default": true
}
```

### Horaires d'ouverture
```json
{
  "monday": {
    "open": "11:00",
    "close": "22:00",
    "is_closed": false,
    "breaks": [
      {"start": "14:30", "end": "18:00"}
    ]
  },
  "tuesday": {
    "open": "11:00",
    "close": "22:00",
    "is_closed": false,
    "breaks": []
  },
  "wednesday": {
    "open": "11:00",
    "close": "22:00",
    "is_closed": false,
    "breaks": []
  },
  "thursday": {
    "open": "11:00",
    "close": "23:00",
    "is_closed": false,
    "breaks": []
  },
  "friday": {
    "open": "11:00",
    "close": "00:00",
    "is_closed": false,
    "breaks": []
  },
  "saturday": {
    "open": "12:00",
    "close": "00:00",
    "is_closed": false,
    "breaks": []
  },
  "sunday": {
    "is_closed": true
  }
}
```

### Options de menu item
```json
{
  "size": {
    "label": "Taille",
    "type": "radio",
    "required": true,
    "choices": [
      {
        "value": "small",
        "label": "Petit (250ml)",
        "price_modifier": 0.00,
        "is_default": false
      },
      {
        "value": "medium",
        "label": "Moyen (400ml)",
        "price_modifier": 1.50,
        "is_default": true
      },
      {
        "value": "large",
        "label": "Grand (600ml)",
        "price_modifier": 2.50,
        "is_default": false
      }
    ]
  },
  "extras": {
    "label": "Suppléments",
    "type": "checkbox",
    "required": false,
    "multiple": true,
    "max_selections": 5,
    "choices": [
      {
        "value": "cheese",
        "label": "Fromage supplémentaire",
        "price_modifier": 1.00
      },
      {
        "value": "bacon",
        "label": "Bacon",
        "price_modifier": 1.50
      },
      {
        "value": "avocado",
        "label": "Avocat",
        "price_modifier": 2.00
      }
    ]
  },
  "cooking": {
    "label": "Cuisson",
    "type": "radio",
    "required": false,
    "choices": [
      {
        "value": "rare",
        "label": "Saignant",
        "price_modifier": 0.00
      },
      {
        "value": "medium",
        "label": "À point",
        "price_modifier": 0.00,
        "is_default": true
      },
      {
        "value": "well_done",
        "label": "Bien cuit",
        "price_modifier": 0.00
      }
    ]
  }
}
```

---

## États et workflows

### Workflow de commande

```
[PENDING] ─────────────────────────────────────────> [CANCELLED]
   │                                                         ↑
   │ Restaurant accepte                                      │
   ↓                                                         │
[CONFIRMED]                                                  │
   │                                                         │
   │ Restaurant commence                                     │
   ↓                                                         │
[PREPARING] ──────────────────────────────────────────────> │
   │                                                         │
   │ Restaurant termine                                      │
   ↓                                                         │
[READY] ──────────────────────────────────────────────────> │
   │                                                         │
   │ Livreur récupère                                        │
   ↓                                                         │
[PICKED_UP] ─────────────────────────────────────────────> │
   │                                                         │
   │ Livreur arrive                                          │
   ↓                                                         │
[DELIVERED]
```

### Statuts de paiement

```python
PAYMENT_STATUS = {
    'pending': 'En attente',
    'processing': 'En cours',
    'paid': 'Payé',
    'failed': 'Échoué',
    'refunded': 'Remboursé',
    'cancelled': 'Annulé'
}
```

### Disponibilité du livreur

```python
DRIVER_AVAILABILITY = {
    'available': 'Disponible',
    'busy': 'En livraison',
    'offline': 'Hors ligne',
    'on_break': 'En pause'
}
```

---

## Validation des données

### Règles de validation

**User** :
- `email` : Format email valide, unique
- `phone_number` : Format international (E.164)
- `latitude` : Entre -90 et 90
- `longitude` : Entre -180 et 180

**Restaurant** :
- `delivery_fee` : >= 0
- `delivery_radius_km` : > 0
- `estimated_delivery_time` : > 0
- `average_rating` : Entre 0 et 5

**MenuItem** :
- `price` : > 0
- `preparation_time` : > 0
- `average_rating` : Entre 0 et 5

**Order** :
- `subtotal`, `delivery_fee`, `tax`, `total_amount` : >= 0
- `total_amount` doit être égal à `subtotal + delivery_fee + tax - discount`

**Rating** (RestaurantReview, DriverRating) :
- `rating`, `overall_rating`, etc. : Entre 1 et 5

**Coupon** :
- `discount_value` : >= 0
- Pour `percentage` : <= 100
- `valid_until` > `valid_from`
- `usage_count` <= `usage_limit` (si défini)

---

## Indexes recommandés

Pour optimiser les performances, voici les indexes recommandés :

```sql
-- Users
CREATE INDEX idx_user_type ON authentication_user(user_type);
CREATE INDEX idx_user_location ON authentication_user(latitude, longitude);

-- Restaurants
CREATE INDEX idx_restaurant_active ON restaurants_restaurant(is_active, is_accepting_orders);
CREATE INDEX idx_restaurant_location ON restaurants_restaurant(latitude, longitude);
CREATE INDEX idx_restaurant_rating ON restaurants_restaurant(average_rating DESC);

-- MenuItems
CREATE INDEX idx_menuitem_available ON restaurants_menuitem(is_available);
CREATE INDEX idx_menuitem_restaurant ON restaurants_menuitem(restaurant_id);
CREATE INDEX idx_menuitem_category ON restaurants_menuitem(category_id);

-- Orders
CREATE INDEX idx_order_customer ON commandes_order(customer_id, created_at DESC);
CREATE INDEX idx_order_restaurant ON commandes_order(restaurant_id, status, created_at DESC);
CREATE INDEX idx_order_driver ON commandes_order(driver_id, status);
CREATE INDEX idx_order_status ON commandes_order(status, created_at DESC);

-- DeliveryTracking
CREATE INDEX idx_tracking_driver ON livraison_deliverytracking(driver_id, created_at DESC);

-- Promotions
CREATE INDEX idx_coupon_code ON promotions_coupon(code);
CREATE INDEX idx_coupon_active ON promotions_coupon(is_active, valid_from, valid_until);
CREATE INDEX idx_promotion_restaurant ON promotions_promotion(restaurant_id, is_active);
```

---

## Conseils d'implémentation pour le mobile

### 1. Gestion du cache local

**Données à cacher** :
- Liste des restaurants (avec TTL de 5 minutes)
- Menu items par restaurant (TTL de 10 minutes)
- Profil utilisateur (invalider lors des modifications)
- Adresses de livraison (sync bidirectionnel)

**Stratégie** :
```javascript
// Redux Persist pour conserver l'état
// RTK Query pour le cache des requêtes API
const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: API_URL }),
  tagTypes: ['User', 'Restaurant', 'Order'],
  endpoints: (builder) => ({
    getRestaurants: builder.query({
      query: () => 'restaurants/',
      providesTags: ['Restaurant'],
      // Cache pendant 5 minutes
      keepUnusedDataFor: 300,
    }),
  }),
});
```

### 2. Optimisation des images

- Utiliser des thumbnails pour les listes
- Lazy loading des images
- Format WebP si supporté
- Placeholder pendant le chargement

### 3. Gestion de la localisation

```javascript
// Demander la permission
// Utiliser geolocation service
// Mettre à jour la position pour les livreurs toutes les 10-15 secondes
// Pour les clients, une seule fois au démarrage
```

### 4. Websockets pour le temps réel

**Événements à écouter** :
- `order.status_changed` : Changement de statut de commande
- `driver.location_updated` : Position du livreur mise à jour
- `order.assigned` : Livreur assigné à la commande
- `notification.new` : Nouvelle notification

### 5. Gestion des erreurs

**Codes d'erreur API** :
- `400` : Validation error
- `401` : Non authentifié
- `403` : Accès refusé
- `404` : Ressource non trouvée
- `409` : Conflit (ex: coupon déjà utilisé)
- `422` : Données invalides
- `500` : Erreur serveur

---

## Exemples de requêtes complètes

### Créer une commande
```json
POST /api/v1/orders/

{
  "restaurant_id": 12,
  "delivery_address": {
    "label": "Maison",
    "address": "123 Rue de la Paix, 75001 Paris",
    "latitude": 48.8566,
    "longitude": 2.3522,
    "instructions": "Digicode : 1234A"
  },
  "items": [
    {
      "menu_item_id": 45,
      "quantity": 2,
      "selected_options": {
        "size": "medium",
        "extras": ["cheese", "bacon"]
      },
      "special_instructions": "Bien cuit"
    },
    {
      "menu_item_id": 52,
      "quantity": 1,
      "selected_options": {},
      "special_instructions": ""
    }
  ],
  "payment_method": "card",
  "coupon_code": "WELCOME10",
  "customer_notes": "Pas d'oignons svp"
}
```

### Mettre à jour la position du livreur
```json
PATCH /api/v1/delivery-tracking/{tracking_id}/location/

{
  "latitude": 48.8580,
  "longitude": 2.3410
}
```

### Valider un coupon
```json
POST /api/v1/coupons/validate/

{
  "code": "WELCOME10",
  "restaurant_id": 12,
  "order_amount": 25.00
}

Response:
{
  "valid": true,
  "discount_amount": 2.50,
  "coupon": {
    "code": "WELCOME10",
    "description": "10% de réduction",
    "discount_type": "percentage"
  }
}
```

---

## Conclusion

Cette référence complète des modèles de données vous permet de comprendre :
- La structure exacte de chaque modèle
- Les relations entre les modèles
- Les formats JSON attendus
- Les workflows et états
- Les contraintes et validations

Utilisez cette documentation pour :
1. Créer vos interfaces TypeScript/JavaScript
2. Implémenter la logique métier côté mobile
3. Valider les données avant envoi à l'API
4. Gérer correctement le cache et la synchronisation
5. Comprendre les workflows de commande et livraison

Pour toute question ou clarification, n'hésitez pas à consulter l'API directement via `/api/v1/swagger/` ou `/api/v1/redoc/`.
