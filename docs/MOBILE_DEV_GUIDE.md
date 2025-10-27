# 📱 GUIDE COMPLET DE DÉVELOPPEMENT MOBILE - Multi-Restaurants App

**Version** : 1.0
**Date** : 2025
**Backend Repository** : https://github.com/urbainBalogou/multi-restaurants-backend
**Backend Branch** : `claude/improve-project-011CUVkqWyhh4o6JfDayLfws`

---

## 🎯 OBJECTIF DE CE DOCUMENT

Ce document est une **documentation technique exhaustive** pour développer une application mobile complète qui s'intègre avec le backend Multi-Restaurants. Il contient **TOUTES** les informations nécessaires pour qu'un développeur (IA ou humain) puisse créer une application mobile professionnelle de A à Z.

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble du projet](#vue-densemble-du-projet)
2. [Stack technique recommandée](#stack-technique-recommandée)
3. [Architecture de l'application](#architecture-de-lapplication)
4. [Configuration initiale](#configuration-initiale)
5. [Authentification et sécurité](#authentification-et-sécurité)
6. [Intégration API](#intégration-api)
7. [Fonctionnalités à implémenter](#fonctionnalités-à-implémenter)
8. [Gestion d'état](#gestion-détat)
9. [Navigation](#navigation)
10. [UI/UX Design](#uiux-design)
11. [Tests](#tests)
12. [Déploiement](#déploiement)
13. [Checklist complète](#checklist-complète)

---

## 🎨 VUE D'ENSEMBLE DU PROJET

### Qu'est-ce que Multi-Restaurants ?

Une **plateforme de livraison de repas multi-restaurants** (type Uber Eats / DoorDash) avec :

- 🍽️ **Clients** : Commandent des repas depuis plusieurs restaurants
- 🏪 **Restaurateurs** : Gèrent leurs menus, commandes et promotions
- 🚗 **Livreurs** : Acceptent et livrent les commandes
- 👨‍💼 **Administrateurs** : Supervisent la plateforme

### Fonctionnalités principales

#### Pour les Clients
- Inscription / Connexion (JWT)
- Recherche de restaurants par proximité
- Consultation de menus avec photos
- Ajout au panier avec options/personnalisations
- Application de codes promo
- Paiement (Cash, Carte, Mobile)
- Suivi en temps réel de la livraison (GPS)
- Historique des commandes
- Notation des restaurants et livreurs
- Gestion des adresses de livraison
- Restaurants favoris

#### Pour les Restaurateurs
- Gestion du profil restaurant
- Gestion des menus et articles
- Réception et gestion des commandes
- Création de promotions
- Statistiques et rapports
- Configuration des zones de livraison

#### Pour les Livreurs
- Activation/désactivation de la disponibilité
- Réception des commandes assignées
- Navigation GPS vers restaurant et client
- Mise à jour du statut de livraison
- Historique des livraisons
- Statistiques de gains (avec pourboires)

---

## 🛠️ STACK TECHNIQUE RECOMMANDÉE

### Option 1 : React Native (Recommandé)

**Avantages** :
- Un seul codebase pour iOS et Android
- Grande communauté
- Excellentes performances
- Accès aux APIs natives

**Stack complète** :
```json
{
  "framework": "React Native 0.72+",
  "navigation": "React Navigation 6",
  "state": "Redux Toolkit + RTK Query",
  "ui": "React Native Paper / NativeBase / Tamagui",
  "maps": "react-native-maps",
  "location": "@react-native-community/geolocation",
  "http": "axios",
  "storage": "@react-native-async-storage/async-storage",
  "notifications": "react-native-firebase",
  "payments": "@stripe/stripe-react-native",
  "images": "react-native-fast-image",
  "forms": "react-hook-form + yup",
  "testing": "Jest + React Native Testing Library"
}
```

### Option 2 : Flutter

**Stack complète** :
```yaml
dependencies:
  flutter_sdk
  provider: ^6.0.0  # State management
  dio: ^5.0.0  # HTTP client
  flutter_secure_storage: ^8.0.0
  google_maps_flutter: ^2.5.0
  geolocator: ^10.0.0
  firebase_messaging: ^14.0.0
  flutter_stripe: ^9.0.0
  cached_network_image: ^3.3.0
```

### Option 3 : iOS Natif (Swift)

**Stack** :
```
- SwiftUI / UIKit
- Combine / RxSwift
- Alamofire (networking)
- Kingfisher (images)
- Firebase (notifications)
- Stripe iOS SDK
- MapKit / Google Maps
```

### Option 4 : Android Natif (Kotlin)

**Stack** :
```
- Jetpack Compose / XML
- Coroutines + Flow
- Retrofit + OkHttp
- Coil (images)
- Firebase (notifications)
- Stripe Android SDK
- Google Maps SDK
```

---

## 🏗️ ARCHITECTURE DE L'APPLICATION

### Structure de dossiers recommandée (React Native)

```
multi-restaurants-mobile/
├── src/
│   ├── api/                      # Configuration API et endpoints
│   │   ├── client.js            # Axios instance
│   │   ├── endpoints.js         # URLs des endpoints
│   │   └── services/            # Services API par domaine
│   │       ├── authService.js
│   │       ├── restaurantService.js
│   │       ├── orderService.js
│   │       ├── deliveryService.js
│   │       └── promotionService.js
│   │
│   ├── store/                   # Redux store
│   │   ├── index.js
│   │   └── slices/
│   │       ├── authSlice.js
│   │       ├── cartSlice.js
│   │       ├── restaurantSlice.js
│   │       ├── orderSlice.js
│   │       └── userSlice.js
│   │
│   ├── screens/                 # Écrans de l'app
│   │   ├── auth/
│   │   │   ├── LoginScreen.js
│   │   │   ├── RegisterScreen.js
│   │   │   └── ForgotPasswordScreen.js
│   │   ├── customer/
│   │   │   ├── HomeScreen.js
│   │   │   ├── RestaurantListScreen.js
│   │   │   ├── RestaurantDetailScreen.js
│   │   │   ├── MenuItemDetailScreen.js
│   │   │   ├── CartScreen.js
│   │   │   ├── CheckoutScreen.js
│   │   │   ├── OrderTrackingScreen.js
│   │   │   ├── OrderHistoryScreen.js
│   │   │   └── ProfileScreen.js
│   │   ├── restaurant/
│   │   │   ├── RestaurantDashboardScreen.js
│   │   │   ├── MenuManagementScreen.js
│   │   │   ├── OrderManagementScreen.js
│   │   │   ├── PromotionManagementScreen.js
│   │   │   └── StatisticsScreen.js
│   │   └── driver/
│   │       ├── DriverDashboardScreen.js
│   │       ├── DeliveryMapScreen.js
│   │       ├── DeliveryHistoryScreen.js
│   │       └── EarningsScreen.js
│   │
│   ├── components/              # Composants réutilisables
│   │   ├── common/
│   │   │   ├── Button.js
│   │   │   ├── Input.js
│   │   │   ├── Card.js
│   │   │   ├── Loading.js
│   │   │   └── ErrorBoundary.js
│   │   ├── restaurant/
│   │   │   ├── RestaurantCard.js
│   │   │   ├── MenuItemCard.js
│   │   │   └── RestaurantHeader.js
│   │   ├── order/
│   │   │   ├── OrderCard.js
│   │   │   ├── OrderStatusBadge.js
│   │   │   └── OrderTimeline.js
│   │   └── cart/
│   │       ├── CartItem.js
│   │       ├── CartSummary.js
│   │       └── CouponInput.js
│   │
│   ├── navigation/              # Navigation
│   │   ├── AppNavigator.js
│   │   ├── AuthNavigator.js
│   │   ├── CustomerNavigator.js
│   │   ├── RestaurantNavigator.js
│   │   └── DriverNavigator.js
│   │
│   ├── hooks/                   # Custom hooks
│   │   ├── useAuth.js
│   │   ├── useLocation.js
│   │   ├── useDebounce.js
│   │   └── useNotifications.js
│   │
│   ├── utils/                   # Utilitaires
│   │   ├── validators.js
│   │   ├── formatters.js
│   │   ├── constants.js
│   │   ├── permissions.js
│   │   └── helpers.js
│   │
│   ├── assets/                  # Assets statiques
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── theme/                   # Thème et styles
│   │   ├── colors.js
│   │   ├── typography.js
│   │   ├── spacing.js
│   │   └── theme.js
│   │
│   └── config/                  # Configuration
│       ├── env.js
│       ├── firebase.js
│       └── stripe.js
│
├── __tests__/                   # Tests
├── android/                     # Code natif Android
├── ios/                         # Code natif iOS
├── .env.example
├── .gitignore
├── app.json
├── babel.config.js
├── metro.config.js
├── package.json
└── README.md
```

### Architecture en couches

```
┌─────────────────────────────────────┐
│         Presentation Layer          │
│    (Screens, Components, UI)        │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│          Business Logic Layer       │
│      (Hooks, Utils, Validators)     │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│          State Management           │
│         (Redux / Context)           │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│           Data Layer                │
│      (API Services, Storage)        │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│         Backend API                 │
│  (Django REST Framework)            │
└─────────────────────────────────────┘
```

---

## ⚙️ CONFIGURATION INITIALE

### 1. Créer le projet React Native

```bash
# Avec React Native CLI (recommandé pour cette app)
npx react-native init MultiRestaurants --template react-native-template-typescript

# OU avec Expo (plus simple mais moins flexible)
npx create-expo-app MultiRestaurants --template
```

### 2. Installer les dépendances essentielles

```bash
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install @reduxjs/toolkit react-redux
npm install axios react-native-async-storage
npm install react-native-paper react-native-vector-icons
npm install react-native-maps react-native-geolocation-service
npm install @react-native-firebase/app @react-native-firebase/messaging
npm install @stripe/stripe-react-native
npm install react-native-fast-image
npm install react-hook-form yup @hookform/resolvers
npm install react-native-dotenv
npm install date-fns

# Dev dependencies
npm install --save-dev @testing-library/react-native jest
```

### 3. Configuration .env

Créer `.env` :

```env
# API Configuration
API_BASE_URL=http://10.0.2.2:8000  # Android Emulator
# API_BASE_URL=http://localhost:8000  # iOS Simulator
# API_BASE_URL=https://api.multi-restaurants.com  # Production

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key

# Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Firebase
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_PROJECT_ID=your_firebase_project_id

# App Configuration
APP_NAME=MultiRestaurants
APP_VERSION=1.0.0
```

### 4. Configuration des permissions

**android/app/src/main/AndroidManifest.xml** :
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.CAMERA" />
```

**ios/MultiRestaurants/Info.plist** :
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Nous avons besoin de votre localisation pour trouver les restaurants près de vous</string>
<key>NSLocationAlwaysUsageDescription</key>
<string>Votre localisation est utilisée pour le suivi des livraisons</string>
<key>NSCameraUsageDescription</key>
<string>Prendre des photos pour votre profil</string>
```

---

## 🔐 AUTHENTIFICATION ET SÉCURITÉ

### Flow d'authentification JWT

1. **Inscription** → Obtenir access_token + refresh_token
2. **Stocker les tokens** de manière sécurisée
3. **Inclure access_token** dans chaque requête API
4. **Gérer l'expiration** : refresh automatique
5. **Déconnexion** : Supprimer les tokens

### Implémentation recommandée

**src/api/client.js** :
```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_BASE_URL } from '@env';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur de requête - Ajouter le token
apiClient.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Intercepteur de réponse - Gérer le refresh token
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Si erreur 401 et pas déjà une tentative de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');

        // Appeler l'endpoint de refresh
        const response = await axios.post(
          `${API_BASE_URL}/api/auth/token/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;

        // Sauvegarder le nouveau token
        await AsyncStorage.setItem('access_token', access);

        // Refaire la requête originale
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed → Déconnecter l'utilisateur
        await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
        // Navigate to login
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
```

**src/api/services/authService.js** :
```javascript
import apiClient from '../client';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const authService = {
  // Inscription
  register: async (userData) => {
    const response = await apiClient.post('/api/auth/register/', userData);
    return response.data;
  },

  // Connexion
  login: async (credentials) => {
    const response = await apiClient.post('/api/auth/login/', {
      identifiant: credentials.email,
      password: credentials.password,
    });

    const { data } = response.data;

    // Sauvegarder les tokens et user
    await AsyncStorage.setItem('access_token', data.api_token);
    await AsyncStorage.setItem('user', JSON.stringify(data));

    return data;
  },

  // Déconnexion
  logout: async () => {
    await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
  },

  // Vérifier si l'utilisateur est connecté
  isAuthenticated: async () => {
    const token = await AsyncStorage.getItem('access_token');
    return !!token;
  },

  // Obtenir l'utilisateur actuel
  getCurrentUser: async () => {
    const userJson = await AsyncStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
  },
};
```

---

## 🌐 INTÉGRATION API

### Configuration des endpoints

**src/api/endpoints.js** :
```javascript
export const ENDPOINTS = {
  // Authentication
  AUTH: {
    REGISTER: '/api/auth/register/',
    LOGIN: '/api/auth/login/',
    USER: '/api/auth/user/',
  },

  // Restaurants
  RESTAURANTS: {
    LIST: '/api/v1/restaurants/',
    DETAIL: (id) => `/api/v1/restaurants/${id}/`,
    MENU: (id) => `/api/v1/restaurants/${id}/menu/`,
    REVIEWS: (id) => `/api/v1/restaurants/${id}/reviews/`,
    POPULAR: '/api/v1/restaurants/popular/',
    NEARBY: '/api/v1/restaurants/', // + ?lat=XX&lng=YY
  },

  // Menu Items
  MENU_ITEMS: {
    LIST: '/api/v1/menu-items/',
    DETAIL: (id) => `/api/v1/menu-items/${id}/`,
  },

  // Categories
  CATEGORIES: {
    LIST: '/api/v1/categories/',
    MENUS: (id) => `/api/v1/categories/${id}/menus/`,
  },

  // Orders
  ORDERS: {
    LIST: '/api/v1/orders/',
    CREATE: '/api/v1/orders/',
    DETAIL: (id) => `/api/v1/orders/${id}/`,
    STATUS: (id) => `/api/v1/orders/${id}/status/`,
  },

  // Promotions
  PROMOTIONS: {
    COUPONS: '/api/v1/coupons/',
    VALIDATE: '/api/v1/coupons/validate/',
    MY_COUPONS: '/api/v1/coupons/my_coupons/',
    LIST: '/api/v1/promotions/',
    ACTIVE: '/api/v1/promotions/active_now/',
  },

  // Delivery
  DELIVERY: {
    TRACKING: (orderId) => `/api/v1/livraison/tracking/${orderId}/`,
    UPDATE_LOCATION: (trackingId) => `/api/v1/livraison/tracking/${trackingId}/update_location/`,
  },

  // Health
  HEALTH: '/api/v1/health/',
};
```

### Services API complets

**src/api/services/restaurantService.js** :
```javascript
import apiClient from '../client';
import { ENDPOINTS } from '../endpoints';

export const restaurantService = {
  // Obtenir la liste des restaurants
  getRestaurants: async (params = {}) => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.LIST, { params });
    return response.data;
  },

  // Restaurants à proximité
  getNearbyRestaurants: async (latitude, longitude, radius = 10) => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.NEARBY, {
      params: { lat: latitude, lng: longitude, radius },
    });
    return response.data;
  },

  // Détail d'un restaurant
  getRestaurantDetail: async (restaurantId) => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.DETAIL(restaurantId));
    return response.data;
  },

  // Menu d'un restaurant
  getRestaurantMenu: async (restaurantId) => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.MENU(restaurantId));
    return response.data;
  },

  // Avis d'un restaurant
  getRestaurantReviews: async (restaurantId, page = 1) => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.REVIEWS(restaurantId), {
      params: { page },
    });
    return response.data;
  },

  // Restaurants populaires
  getPopularRestaurants: async () => {
    const response = await apiClient.get(ENDPOINTS.RESTAURANTS.POPULAR);
    return response.data;
  },

  // Ajouter un avis
  addReview: async (restaurantId, reviewData) => {
    const response = await apiClient.post(
      ENDPOINTS.RESTAURANTS.REVIEWS(restaurantId),
      reviewData
    );
    return response.data;
  },
};
```

Continuons avec les autres fichiers de documentation...

**SUITE DU DOCUMENT** →

Je continue la documentation complète dans les prochains fichiers...
