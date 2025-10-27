# 📡 RÉFÉRENCE API COMPLÈTE - Multi-Restaurants Backend

**Base URL** : `http://localhost:8000` (dev) | `https://api.multi-restaurants.com` (prod)

---

## 🔐 AUTHENTIFICATION

### 1. Inscription (Register)

**Endpoint** : `POST /api/auth/register/`

**Body** :
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "customer",
  "phone_number": "+33612345678",
  "address": "123 Rue de Paris, 75001 Paris",
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

**Response 201** :
```json
{
  "message": "Inscription réussie",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "user_type": "customer",
    "phone_number": "+33612345678",
    "api_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Errors** :
- `400` : Données invalides
- `409` : Email/username déjà existant

---

### 2. Connexion (Login)

**Endpoint** : `POST /api/auth/login/`

**Body** :
```json
{
  "identifiant": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response 200** :
```json
{
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "user_type": "customer",
    "api_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Errors** :
- `400` : Identifiants invalides
- `401` : Authentification échouée

---

### 3. Obtenir le profil utilisateur

**Endpoint** : `GET /api/auth/user/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Response 200** :
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "customer",
  "phone_number": "+33612345678",
  "address": "123 Rue de Paris",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "is_active": true,
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## 🍽️ RESTAURANTS

### 1. Liste des restaurants

**Endpoint** : `GET /api/v1/restaurants/`

**Query Parameters** :
- `page` (int) : Numéro de page (défaut: 1)
- `search` (string) : Recherche textuelle
- `is_accepting_orders` (boolean) : Filtre commandes acceptées
- `ordering` (string) : Tri (`average_rating`, `-created_at`, etc.)

**Example** : `GET /api/v1/restaurants/?page=1&search=pizza&ordering=-average_rating`

**Response 200** :
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/v1/restaurants/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Pizza Roma",
      "description": "Pizzeria italienne authentique",
      "image": "http://localhost:8000/media/restaurants/pizza_roma.jpg",
      "address": "15 Rue de la Paix, Paris",
      "latitude": 48.8698,
      "longitude": 2.3282,
      "phone_number": "+33140123456",
      "average_rating": 4.5,
      "total_reviews": 234,
      "delivery_fee": "2.50",
      "free_delivery_threshold": "20.00",
      "estimated_delivery_time": 30,
      "is_active": true,
      "is_accepting_orders": true
    }
  ]
}
```

---

### 2. Restaurants à proximité

**Endpoint** : `GET /api/v1/restaurants/?lat=<latitude>&lng=<longitude>&radius=<km>`

**Example** : `GET /api/v1/restaurants/?lat=48.8566&lng=2.3522&radius=5`

**Response 200** :
```json
{
  "results": [
    {
      "id": 1,
      "name": "Pizza Roma",
      "distance_km": 1.2,
      "average_rating": 4.5,
      "delivery_fee": "2.50",
      "estimated_delivery_time": 25,
      ...
    },
    {
      "id": 2,
      "name": "Sushi Paradise",
      "distance_km": 2.8,
      "average_rating": 4.7,
      ...
    }
  ]
}
```

---

### 3. Détail d'un restaurant

**Endpoint** : `GET /api/v1/restaurants/<id>/`

**Example** : `GET /api/v1/restaurants/1/`

**Response 200** :
```json
{
  "id": 1,
  "owner": {
    "id": 5,
    "username": "restaurant_owner",
    "email": "owner@pizzaroma.com"
  },
  "name": "Pizza Roma",
  "description": "Pizzeria italienne authentique avec des ingrédients frais",
  "image": "http://localhost:8000/media/restaurants/pizza_roma.jpg",
  "address": "15 Rue de la Paix, 75002 Paris",
  "latitude": 48.8698,
  "longitude": 2.3282,
  "phone_number": "+33140123456",
  "email": "contact@pizzaroma.com",
  "opening_hours": {
    "lundi": {"open": "11:00", "close": "23:00"},
    "mardi": {"open": "11:00", "close": "23:00"},
    "mercredi": {"open": "11:00", "close": "23:00"},
    "jeudi": {"open": "11:00", "close": "23:00"},
    "vendredi": {"open": "11:00", "close": "01:00"},
    "samedi": {"open": "11:00", "close": "01:00"},
    "dimanche": {"closed": true}
  },
  "is_active": true,
  "is_accepting_orders": true,
  "average_rating": 4.5,
  "total_reviews": 234,
  "delivery_fee": "2.50",
  "free_delivery_threshold": "20.00",
  "delivery_radius_km": 5.0,
  "estimated_delivery_time": 30,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2025-01-15T15:30:00Z"
}
```

---

### 4. Menu d'un restaurant

**Endpoint** : `GET /api/v1/restaurants/<id>/menu/`

**Example** : `GET /api/v1/restaurants/1/menu/`

**Response 200** :
```json
[
  {
    "category": {
      "id": 1,
      "name": "Pizzas",
      "description": "Nos pizzas artisanales",
      "image": "http://localhost:8000/media/categories/pizzas.jpg",
      "order": 1
    },
    "items": [
      {
        "id": 1,
        "name": "Pizza Margherita",
        "description": "Tomate, mozzarella, basilic frais",
        "price": "12.50",
        "image": "http://localhost:8000/media/menu_items/margherita.jpg",
        "is_available": true,
        "preparation_time": 15,
        "calories": 850,
        "allergens": ["gluten", "lactose"],
        "has_options": true,
        "options": {
          "taille": [
            {"name": "Petite", "price": "0.00"},
            {"name": "Moyenne", "price": "2.00"},
            {"name": "Grande", "price": "4.00"}
          ],
          "supplements": [
            {"name": "Fromage extra", "price": "1.50"},
            {"name": "Olives", "price": "1.00"}
          ]
        },
        "average_rating": 4.6,
        "order_count": 456
      }
    ]
  },
  {
    "category": {
      "id": 2,
      "name": "Desserts",
      ...
    },
    "items": [...]
  }
]
```

---

### 5. Avis d'un restaurant

**Endpoint** : `GET /api/v1/restaurants/<id>/reviews/`

**Response 200** :
```json
{
  "count": 234,
  "next": "http://localhost:8000/api/v1/restaurants/1/reviews/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "customer": {
        "id": 3,
        "username": "marie_martin",
        "first_name": "Marie"
      },
      "rating": 5,
      "comment": "Excellente pizza ! Service rapide et sympathique.",
      "created_at": "2025-01-14T19:45:00Z"
    },
    {
      "id": 2,
      "customer": {
        "id": 7,
        "username": "pierre_dupont"
      },
      "rating": 4,
      "comment": "Très bon mais un peu cher",
      "created_at": "2025-01-13T20:15:00Z"
    }
  ]
}
```

---

### 6. Restaurants populaires

**Endpoint** : `GET /api/v1/restaurants/popular/`

**Response 200** :
```json
[
  {
    "id": 3,
    "name": "Burger King Premium",
    "average_rating": 4.8,
    "total_reviews": 1245,
    "image": "...",
    ...
  },
  ...
]
```

---

## 📦 COMMANDES

### 1. Créer une commande

**Endpoint** : `POST /api/v1/orders/`

**Headers** :
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body** :
```json
{
  "restaurant": 1,
  "items": [
    {
      "menu_item": 5,
      "quantity": 2,
      "unit_price": "12.50",
      "selected_options": {
        "taille": "Grande",
        "supplements": ["Fromage extra", "Olives"]
      },
      "special_instructions": "Bien cuite SVP"
    },
    {
      "menu_item": 12,
      "quantity": 1,
      "unit_price": "5.00",
      "selected_options": {},
      "special_instructions": ""
    }
  ],
  "delivery_address": {
    "street": "25 Avenue des Champs-Élysées",
    "city": "Paris",
    "postal_code": "75008",
    "country": "France",
    "instructions": "Appartement 3B, 2ème étage"
  },
  "delivery_latitude": 48.8698,
  "delivery_longitude": 2.3081,
  "payment_method": "card",
  "customer_notes": "Merci de sonner 2 fois",
  "coupon_code": "FIRST20"
}
```

**Response 201** :
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "order_number": "12345678",
  "customer": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "restaurant": {
    "id": 1,
    "name": "Pizza Roma",
    "phone_number": "+33140123456"
  },
  "items": [
    {
      "id": 1,
      "menu_item": {
        "id": 5,
        "name": "Pizza Margherita",
        "image": "..."
      },
      "quantity": 2,
      "unit_price": "12.50",
      "total_price": "25.00",
      "selected_options": {
        "taille": "Grande",
        "supplements": ["Fromage extra", "Olives"]
      },
      "special_instructions": "Bien cuite SVP"
    }
  ],
  "status": "pending",
  "subtotal": "30.00",
  "delivery_fee": "2.50",
  "tax": "3.25",
  "discount": "6.00",
  "total_amount": "29.75",
  "payment_method": "card",
  "payment_status": "pending",
  "delivery_address": {
    "street": "25 Avenue des Champs-Élysées",
    "city": "Paris",
    "postal_code": "75008",
    "country": "France"
  },
  "delivery_latitude": 48.8698,
  "delivery_longitude": 2.3081,
  "estimated_delivery_time": "2025-01-15T12:45:00Z",
  "created_at": "2025-01-15T12:00:00Z"
}
```

---

### 2. Liste de mes commandes

**Endpoint** : `GET /api/v1/orders/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Query Parameters** :
- `status` : Filtrer par statut (pending, confirmed, preparing, etc.)
- `page` : Pagination

**Example** : `GET /api/v1/orders/?status=delivered&page=1`

**Response 200** :
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/v1/orders/?page=2",
  "previous": null,
  "results": [
    {
      "id": "a1b2c3d4-...",
      "order_number": "12345678",
      "restaurant": {
        "id": 1,
        "name": "Pizza Roma",
        "image": "..."
      },
      "status": "delivered",
      "total_amount": "29.75",
      "created_at": "2025-01-15T12:00:00Z",
      "delivered_at": "2025-01-15T12:45:00Z"
    },
    ...
  ]
}
```

---

### 3. Détail d'une commande

**Endpoint** : `GET /api/v1/orders/<order_id>/`

**Example** : `GET /api/v1/orders/a1b2c3d4-e5f6-7890-abcd-ef1234567890/`

**Response 200** :
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "order_number": "12345678",
  "customer": {...},
  "restaurant": {...},
  "driver": {
    "id": 8,
    "username": "driver_jean",
    "phone_number": "+33698765432",
    "vehicle_type": "scooter"
  },
  "items": [...],
  "status": "picked_up",
  "subtotal": "30.00",
  "delivery_fee": "2.50",
  "tax": "3.25",
  "total_amount": "29.75",
  "payment_method": "card",
  "payment_status": "paid",
  "delivery_address": {...},
  "estimated_delivery_time": "2025-01-15T12:45:00Z",
  "actual_delivery_time": null,
  "customer_notes": "Merci de sonner 2 fois",
  "tracking": {
    "current_latitude": 48.8650,
    "current_longitude": 2.3100,
    "distance_remaining_km": 1.2,
    "estimated_arrival": "2025-01-15T12:42:00Z"
  },
  "created_at": "2025-01-15T12:00:00Z",
  "updated_at": "2025-01-15T12:35:00Z"
}
```

---

### 4. Mettre à jour le statut d'une commande

**Endpoint** : `PATCH /api/v1/orders/<order_id>/status/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Body** :
```json
{
  "status": "confirmed"
}
```

**Statuts possibles** :
- `pending` → `confirmed` (restaurant)
- `confirmed` → `preparing` (restaurant)
- `preparing` → `ready` (restaurant)
- `ready` → `picked_up` (livreur)
- `picked_up` → `delivered` (livreur)
- `*` → `cancelled` (client/restaurant avant picked_up)

**Response 200** :
```json
{
  "id": "a1b2c3d4-...",
  "status": "confirmed",
  "updated_at": "2025-01-15T12:05:00Z"
}
```

---

## 🎁 PROMOTIONS & COUPONS

### 1. Liste des coupons disponibles

**Endpoint** : `GET /api/v1/coupons/`

**Response 200** :
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "code": "FIRST20",
      "description": "20% de réduction sur votre première commande",
      "discount_type": "percentage",
      "discount_value": "20.00",
      "min_order_amount": "15.00",
      "max_discount_amount": "10.00",
      "valid_from": "2025-01-01T00:00:00Z",
      "valid_until": "2025-12-31T23:59:59Z",
      "usage_limit": 1000,
      "usage_limit_per_user": 1,
      "usage_count": 234,
      "is_active": true
    },
    {
      "id": 2,
      "code": "FREEDELIVERY",
      "description": "Livraison gratuite",
      "discount_type": "free_delivery",
      "discount_value": "0.00",
      "min_order_amount": "20.00",
      ...
    }
  ]
}
```

---

### 2. Valider un coupon

**Endpoint** : `POST /api/v1/coupons/validate/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Body** :
```json
{
  "code": "FIRST20",
  "order_amount": 45.00,
  "restaurant_id": 1
}
```

**Response 200** :
```json
{
  "valid": true,
  "message": "Code promo valide",
  "coupon": {
    "id": 1,
    "code": "FIRST20",
    "discount_type": "percentage",
    "discount_value": "20.00"
  },
  "discount_amount": 9.00,
  "free_delivery": false
}
```

**Response 400** (invalide) :
```json
{
  "valid": false,
  "message": "Le coupon a expiré"
}
```

---

### 3. Mes coupons disponibles

**Endpoint** : `GET /api/v1/coupons/my_coupons/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Response 200** :
```json
[
  {
    "id": 3,
    "code": "WELCOME10",
    "description": "10€ de réduction pour les nouveaux clients",
    "discount_type": "fixed",
    "discount_value": "10.00",
    "min_order_amount": "30.00",
    "valid_until": "2025-02-28T23:59:59Z"
  }
]
```

---

### 4. Promotions actives

**Endpoint** : `GET /api/v1/promotions/active_now/`

**Response 200** :
```json
[
  {
    "id": 1,
    "restaurant": {
      "id": 1,
      "name": "Pizza Roma"
    },
    "name": "Happy Hour",
    "description": "30% de réduction sur toutes les pizzas de 18h à 20h",
    "promotion_type": "percentage",
    "discount_value": "30.00",
    "valid_from": "2025-01-01T00:00:00Z",
    "valid_until": "2025-01-31T23:59:59Z",
    "applicable_days": [0, 1, 2, 3, 4],
    "start_time": "18:00:00",
    "end_time": "20:00:00",
    "image": "http://localhost:8000/media/promotions/happy_hour.jpg"
  }
]
```

---

## 🚗 LIVRAISON & TRACKING

### 1. Suivi d'une commande

**Endpoint** : `GET /api/v1/livraison/tracking/<order_id>/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Response 200** :
```json
{
  "order_id": "a1b2c3d4-...",
  "driver": {
    "id": 8,
    "username": "driver_jean",
    "phone_number": "+33698765432",
    "vehicle_type": "scooter",
    "average_rating": 4.7
  },
  "current_latitude": 48.8650,
  "current_longitude": 2.3100,
  "last_location_update": "2025-01-15T12:40:15Z",
  "estimated_arrival": "2025-01-15T12:45:00Z",
  "distance_remaining_km": 1.2,
  "picked_up_at": "2025-01-15T12:30:00Z",
  "delivered_at": null
}
```

---

### 2. Mettre à jour la position (livreur)

**Endpoint** : `PATCH /api/v1/livraison/tracking/<tracking_id>/update_location/`

**Headers** :
```
Authorization: Bearer <access_token>
```

**Body** :
```json
{
  "latitude": 48.8655,
  "longitude": 2.3105
}
```

**Response 200** :
```json
{
  "current_latitude": 48.8655,
  "current_longitude": 2.3105,
  "last_location_update": "2025-01-15T12:41:30Z",
  "distance_remaining_km": 1.0
}
```

---

## 📊 CATÉGORIES & MENU ITEMS

### 1. Liste des catégories

**Endpoint** : `GET /api/v1/categories/`

**Response 200** :
```json
[
  {
    "id": 1,
    "name": "Pizzas",
    "description": "Pizzas artisanales",
    "image": "http://localhost:8000/media/categories/pizzas.jpg",
    "is_active": true,
    "order": 1
  },
  {
    "id": 2,
    "name": "Burgers",
    ...
  }
]
```

---

### 2. Menu items d'une catégorie

**Endpoint** : `GET /api/v1/categories/<id>/menus/`

**Response 200** :
```json
{
  "category": {
    "id": 1,
    "name": "Pizzas",
    ...
  },
  "data": [
    {
      "id": 1,
      "restaurant": {
        "id": 1,
        "name": "Pizza Roma"
      },
      "name": "Pizza Margherita",
      "price": "12.50",
      ...
    }
  ],
  "count": 15
}
```

---

## 🏥 HEALTH CHECK

**Endpoint** : `GET /api/v1/health/`

**Response 200** :
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T12:00:00.000Z"
}
```

---

## 🚨 GESTION DES ERREURS

### Codes d'erreur standards

- `200` : Succès
- `201` : Créé avec succès
- `204` : Succès sans contenu
- `400` : Mauvaise requête (données invalides)
- `401` : Non authentifié
- `403` : Accès interdit
- `404` : Ressource non trouvée
- `409` : Conflit (ex: email existant)
- `500` : Erreur serveur

### Format des erreurs

```json
{
  "message": "Erreurs de validation",
  "errors": {
    "email": ["Cette adresse email existe déjà"],
    "password": ["Le mot de passe doit contenir au moins 8 caractères"]
  }
}
```

---

## 📝 NOTES IMPORTANTES

### Authentification
- Tous les endpoints (sauf login/register) nécessitent un token JWT
- Format du header : `Authorization: Bearer <token>`
- Token expire après 60 minutes
- Utiliser le refresh token pour obtenir un nouveau token

### Pagination
- Par défaut : 20 items par page
- Paramètre : `?page=<num>`
- Response contient : `count`, `next`, `previous`, `results`

### Filtrage et recherche
- Utiliser `?search=<terme>` pour recherche textuelle
- Filtres spécifiques selon l'endpoint
- Tri avec `?ordering=<field>` (préfixer `-` pour desc)

### Formats de date
- ISO 8601 : `2025-01-15T12:00:00Z`
- Timezone : UTC

### Upload d'images
- Format : multipart/form-data
- Taille max : 5MB
- Formats acceptés : JPG, PNG, WebP

---

**FIN DE LA RÉFÉRENCE API**

Consultez également :
- MOBILE_DEV_GUIDE.md pour l'implémentation
- CODE_EXAMPLES.md pour des exemples détaillés
- DATA_MODELS_REFERENCE.md pour les structures de données
