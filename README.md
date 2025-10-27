# 🍔 Multi-Restaurants Backend

**Plateforme complète de livraison de repas multi-restaurants** - Backend Django REST API professionnel pour une solution type Uber Eats / DoorDash.

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)

---

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Technologies](#-technologies)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API Documentation](#-api-documentation)
- [Tests](#-tests)
- [Déploiement](#-déploiement)
- [Contribution](#-contribution)
- [License](#-license)

---

## ✨ Fonctionnalités

### 🔐 Authentification & Utilisateurs
- **Multi-rôles** : Client, Restaurateur, Livreur, Administrateur
- **JWT Authentication** avec refresh tokens
- **Profils personnalisés** pour clients et livreurs
- **Gestion des favoris** et adresses de livraison

### 🍽️ Gestion des Restaurants
- **CRUD complet** pour restaurants et menus
- **Catégories de plats** avec images
- **Options et personnalisations** des articles
- **Informations nutritionnelles** et allergènes
- **Système de notation** et avis clients
- **Zones de livraison** avec calcul de frais
- **Horaires d'ouverture** flexibles (JSON)

### 📦 Gestion des Commandes
- **Cycle de vie complet** : En attente → Confirmée → En préparation → Prête → Récupérée → Livrée
- **Calculs automatiques** : sous-total, taxes, frais de livraison
- **Paiement multi-méthodes** : Cash, Carte, Mobile
- **Notes spéciales** pour restaurant et livreur
- **Historique des commandes**

### 🚗 Système de Livraison
- **Attribution automatique** des livreurs (algorithme de proximité)
- **Suivi GPS en temps réel** de la livraison
- **Estimation du temps d'arrivée** (ETA)
- **Zones de livraison** configurables par restaurant
- **Évaluation des livreurs** avec notes détaillées
- **Système de pourboires**

### 🎁 Promotions & Coupons
- **Codes promo** : pourcentage, montant fixe, livraison gratuite
- **Promotions restaurant** : réductions temporaires, happy hours
- **Buy X Get Y** : offres spéciales
- **Restrictions** : montant minimum, restaurants spécifiques, utilisateurs VIP
- **Limites d'utilisation** par utilisateur et globale
- **Validité temporelle** avec jours et heures applicables

### 📧 Notifications
- **Emails automatiques** via Celery :
  - Confirmation de commande
  - Mises à jour de statut
  - Attribution au livreur
  - Statistiques quotidiennes aux restaurateurs
- **Support SMS** (Twilio intégré)
- **Notifications push** (architecture prête)

### 🔍 Recherche & Filtres
- **Recherche par proximité** (géolocalisation)
- **Filtres avancés** : catégorie, prix, note, temps de livraison
- **Tri** : distance, popularité, note, prix
- **Recherche textuelle** dans les restaurants et menus

### 📊 Fonctionnalités Avancées
- **Rate Limiting** et throttling API
- **Pagination** personnalisable
- **Logging professionnel** avec rotation
- **Health checks** pour monitoring
- **Documentation Swagger** interactive
- **Support AWS S3** pour les médias
- **Tâches asynchrones** (Celery + Redis)

---

## 🛠️ Technologies

### Backend
- **Django 5.2.6** - Framework web Python
- **Django REST Framework 3.16.1** - API RESTful
- **PostgreSQL 15** - Base de données relationnelle
- **Redis 7** - Cache et message broker
- **Celery 5.5.3** - Tâches asynchrones

### Sécurité & Auth
- **JWT (Simple JWT)** - Authentification par tokens
- **python-decouple** - Gestion des variables d'environnement
- **CORS Headers** - Gestion Cross-Origin

### Géolocalisation
- **GeoPy 2.4.1** - Calculs de distance
- **GeographicLib** - Calculs géographiques avancés

### Paiement
- **Stripe 11.3.0** - Passerelle de paiement

### Cloud & Storage
- **Boto3** - Intégration AWS S3
- **django-storages** - Gestion des médias cloud

### Documentation & Tests
- **drf-yasg** - Documentation Swagger/OpenAPI
- **pytest** - Framework de tests
- **coverage** - Couverture de code
- **factory-boy** - Génération de données de test
- **Faker** - Données fictives

### DevOps
- **Docker & Docker Compose** - Conteneurisation
- **Nginx** - Reverse proxy
- **Gunicorn** - Serveur WSGI
- **Sentry** - Monitoring et error tracking

---

## 🏗️ Architecture

```
multi-restaurants-backend/
├── apps/                          # Applications Django
│   ├── authentication/            # Utilisateurs et profils
│   │   ├── models.py             # User, CustomerProfile, DriverProfile
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── restaurants/               # Restaurants et menus
│   │   ├── models.py             # Restaurant, MenuItem, Category, Review
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── permissions.py
│   ├── commandes/                 # Système de commandes
│   │   ├── models.py             # Order, OrderItem
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── signals.py
│   │   └── tasks.py              # Tâches Celery
│   ├── livraison/                 # Livraison et tracking
│   │   ├── models.py             # DeliveryTracking, DeliveryZone, DriverRating
│   │   ├── serializers.py
│   │   └── views.py
│   └── promotions/                # Coupons et promotions
│       ├── models.py             # Coupon, Promotion, CouponUsage
│       ├── serializers.py
│       ├── views.py
│       └── admin.py
├── multi_restaurants/             # Configuration du projet
│   ├── settings.py               # Settings avec decouple
│   ├── urls.py                   # URLs principales
│   ├── celery.py                 # Configuration Celery
│   ├── wsgi.py
│   └── asgi.py
├── nginx/                         # Configuration Nginx
│   ├── nginx.conf
│   └── conf.d/
│       └── app.conf
├── logs/                          # Logs applicatifs
├── media/                         # Fichiers uploadés
├── static/                        # Fichiers statiques
├── Dockerfile                     # Image Docker optimisée
├── docker-compose.yml             # Stack complète
├── requirements.txt               # Dépendances Python
├── .env.example                   # Template variables d'environnement
├── .gitignore
├── manage.py
└── README.md
```

---

## 🚀 Installation

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optionnel mais recommandé)

### Installation locale

```bash
# Cloner le repository
git clone https://github.com/votre-username/multi-restaurants-backend.git
cd multi-restaurants-backend

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Copier le fichier d'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# Migrations
python manage.py makemigrations
python manage.py migrate

# Créer un superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer le serveur de développement
python manage.py runserver
```

### Installation avec Docker 🐳

```bash
# Cloner le repository
git clone https://github.com/votre-username/multi-restaurants-backend.git
cd multi-restaurants-backend

# Copier et configurer .env
cp .env.example .env
# Éditer .env

# Lancer avec Docker Compose
docker-compose up -d

# Migrations dans Docker
docker-compose exec web python manage.py migrate

# Créer un superuser
docker-compose exec web python manage.py createsuperuser

# Accéder à l'application
open http://localhost/swagger/
```

---

## ⚙️ Configuration

### Variables d'environnement (.env)

Consultez `.env.example` pour toutes les variables disponibles.

**Essentielles :**
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_ENGINE=django.db.backends.postgresql
DB_NAME=multi_restaurants_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

STRIPE_SECRET_KEY=sk_test_your_key
```

---

## 📖 Utilisation

### Lancer les services

```bash
# Serveur Django
python manage.py runserver

# Celery Worker (terminal 2)
celery -A multi_restaurants worker -l info

# Celery Beat (terminal 3)
celery -A multi_restaurants beat -l info

# Flower (monitoring Celery - optionnel)
celery -A multi_restaurants flower
```

### Avec Docker

```bash
# Tout est déjà lancé avec docker-compose up
docker-compose ps  # Vérifier l'état des services

# Voir les logs
docker-compose logs -f web
docker-compose logs -f celery_worker
```

---

## 📚 API Documentation

### Documentation interactive

Une fois le serveur lancé :

- **Swagger UI** : http://localhost:8000/swagger/
- **ReDoc** : http://localhost:8000/redoc/
- **Admin Panel** : http://localhost:8000/admin/

### Principaux endpoints

#### Authentication
```
POST   /api/auth/register/           # Inscription
POST   /api/auth/login/              # Connexion
GET    /api/auth/user/               # Profil utilisateur
```

#### Restaurants
```
GET    /api/v1/restaurants/                    # Liste restaurants
POST   /api/v1/restaurants/                    # Créer restaurant
GET    /api/v1/restaurants/{id}/               # Détail restaurant
GET    /api/v1/restaurants/{id}/menu/          # Menu du restaurant
GET    /api/v1/restaurants/{id}/reviews/       # Avis du restaurant
GET    /api/v1/restaurants/popular/            # Restaurants populaires
GET    /api/v1/restaurants/?lat=48.8&lng=2.3   # Recherche proximité
```

#### Commandes
```
GET    /api/v1/orders/               # Mes commandes
POST   /api/v1/orders/               # Créer commande
GET    /api/v1/orders/{id}/          # Détail commande
PATCH  /api/v1/orders/{id}/status/   # Mettre à jour statut
```

#### Promotions
```
GET    /api/v1/coupons/              # Coupons disponibles
POST   /api/v1/coupons/validate/     # Valider un coupon
GET    /api/v1/promotions/           # Promotions actives
```

#### Health Check
```
GET    /api/v1/health/               # Statut du serveur
```

Pour la documentation complète, consultez [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec couverture
pytest --cov=apps --cov-report=html

# Tests spécifiques
pytest apps/authentication/tests.py
pytest apps/restaurants/tests.py -v

# Voir le rapport de couverture
open htmlcov/index.html
```

---

## 🚢 Déploiement

Consultez [INSTALLATION.md](INSTALLATION.md) pour un guide de déploiement complet.

### Déploiement rapide avec Docker

```bash
# En production
docker-compose -f docker-compose.prod.yml up -d

# Avec SSL/HTTPS (Let's Encrypt)
./scripts/setup-ssl.sh votre-domaine.com
```

### Checklist production

- [ ] Configurer les variables d'environnement en production
- [ ] DEBUG=False
- [ ] SECRET_KEY unique et sécurisée
- [ ] Base de données PostgreSQL
- [ ] Redis pour Celery
- [ ] Nginx avec SSL/TLS
- [ ] Collecte des fichiers statiques
- [ ] Configuration CORS restrictive
- [ ] Sentry pour monitoring
- [ ] Backup automatique de la DB
- [ ] Logs rotatifs configurés

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

---

## 📝 License

Projet sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👥 Auteurs

- **Votre Nom** - *Développement initial* - [GitHub](https://github.com/votre-username)

---

## 🙏 Remerciements

- Django & DRF Community
- Anthropic Claude pour l'assistance au développement
- Tous les contributeurs

---

## 📞 Support

Pour toute question ou assistance :

- **Email** : support@multi-restaurants.com
- **Issues** : [GitHub Issues](https://github.com/votre-username/multi-restaurants-backend/issues)
- **Documentation** : [Wiki](https://github.com/votre-username/multi-restaurants-backend/wiki)

---

**Made with ❤️ and Django**
