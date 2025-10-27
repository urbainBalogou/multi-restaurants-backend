# Multi-Restaurants Mobile App - Documentation Complète

> Documentation exhaustive pour le développement de l'application mobile Multi-Restaurants

## Vue d'ensemble

Multi-Restaurants est une plateforme complète de livraison de repas à domicile, similaire à Uber Eats ou Deliveroo. Cette documentation fournit tout ce dont vous avez besoin pour développer l'application mobile from scratch.

### Rôles utilisateurs

L'application supporte **3 rôles principaux** :

1. **Client** 👤
   - Parcourir les restaurants
   - Commander des repas
   - Suivre les livraisons en temps réel
   - Noter restaurants et livreurs

2. **Propriétaire de restaurant** 🍴
   - Gérer le menu et les prix
   - Accepter/refuser les commandes
   - Suivre les performances
   - Créer des promotions

3. **Livreur** 🚴
   - Accepter des courses
   - Navigation GPS
   - Gérer les livraisons
   - Suivre les revenus

---

## Architecture technique

### Stack recommandée

**Frontend Mobile** :
- React Native 0.72+
- TypeScript
- Redux Toolkit + RTK Query
- React Navigation 6

**Backend API** :
- Django 5.2.6 + Django REST Framework
- PostgreSQL
- Redis + Celery
- JWT Authentication

**Services tiers** :
- Google Maps API (cartes et navigation)
- Firebase (push notifications, analytics)
- Stripe (paiements)
- Sentry (error tracking)

### Flux de données

```
Mobile App ──┬─> REST API (Django) ──> PostgreSQL
             │
             ├─> WebSocket Server ──> Real-time updates
             │
             ├─> Google Maps API ──> Géolocalisation
             │
             ├─> Stripe API ──> Paiements
             │
             └─> Firebase ──> Push Notifications
```

---

## Documentation disponible

Cette documentation est organisée en **7 guides spécialisés** :

### 1. 📘 [MOBILE_DEV_GUIDE.md](./MOBILE_DEV_GUIDE.md)
**Guide principal de développement**

- Objectifs et prérequis du projet
- Stack technologique détaillée
- Structure complète des dossiers
- Architecture de l'application (couches, patterns)
- Configuration initiale (dependencies, .env, permissions)
- Authentification JWT (flow complet avec code)
- Intégration API (client HTTP avec interceptors)
- Gestion d'état avec Redux
- Navigation

**À lire en premier** pour comprendre l'architecture globale.

---

### 2. 🔌 [API_COMPLETE_REFERENCE.md](./API_COMPLETE_REFERENCE.md)
**Référence complète de l'API**

Documentation exhaustive de tous les endpoints :
- **Authentication** : Register, Login, Refresh token, Logout, Password reset
- **Restaurants** : List, Search, Detail, Menu, Reviews, Nearby
- **Orders** : Create, List, Detail, Update status, Cancel
- **Promotions** : Coupons, Validate, Active promotions
- **Delivery** : Tracking, Update location, Driver info
- **User** : Profile, Addresses, Favorites

**Chaque endpoint inclut** :
- URL et méthode HTTP
- Headers requis (auth, content-type)
- Request body avec exemple JSON
- Response avec exemple JSON complet
- Codes d'erreur possibles

**Utilisez ce guide** pour implémenter les appels API.

---

### 3. 💻 [CODE_EXAMPLES.md](./CODE_EXAMPLES.md)
**Exemples de code prêts à l'emploi**

Code production-ready pour :
- Configuration du store Redux
- Slices Redux (auth, cart, restaurant, order)
- Services API (authService, restaurantService, orderService)
- Écrans complets (LoginScreen, HomeScreen, RestaurantDetailScreen)
- Composants réutilisables (RestaurantCard, MenuItemCard)
- Hooks personnalisés (useAuth, useCart, useLocation)

**Copiez-collez et adaptez** ce code pour accélérer le développement.

---

### 4. ✅ [FEATURES_CHECKLIST.md](./FEATURES_CHECKLIST.md)
**Checklist complète des fonctionnalités**

Liste exhaustive (~150-200 heures de dev) :
- **Module Authentification** (8 écrans)
- **Module Client** (15+ écrans)
- **Module Restaurant** (10+ écrans)
- **Module Livreur** (8+ écrans)
- **Modules transverses** : Notifications, Géolocalisation, Paiement, Analytics

**Chaque feature inclut** :
- Description détaillée
- Écrans concernés
- Composants nécessaires
- Intégrations API
- Estimation de temps

**Utilisez cette checklist** pour planifier et suivre l'avancement.

---

### 5. 🎨 [UI_UX_GUIDELINES.md](./UI_UX_GUIDELINES.md)
**Guidelines de design UI/UX**

Spécifications complètes pour une interface cohérente :
- **Système de couleurs** (palette complète, mode clair/sombre)
- **Typographie** (échelle, poids, usages)
- **Espacement** (grille 8px, marges, paddings)
- **Composants UI** (boutons, cartes, inputs, badges)
- **Icônes** (bibliothèque recommandée)
- **Animations** (durées, courbes, micro-interactions)
- **Accessibilité** (contraste, tailles tactiles, lecteurs d'écran)
- **Wireframes** (maquettes des écrans principaux)

**Suivez ces guidelines** pour créer une app professionnelle et cohérente.

---

### 6. 🚀 [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
**Guide de déploiement complet**

Tout ce qu'il faut pour déployer sur les stores :

**Configuration** :
- Comptes développeurs (Apple, Google)
- Certificats et signing
- Variables d'environnement production

**Build** :
- iOS (Xcode, archives, IPA)
- Android (Gradle, AAB, APK)
- Optimisation de la taille

**Stores** :
- App Store Connect (métadonnées, screenshots, soumission)
- Google Play Console (fiche store, déploiement progressif)
- Tests Beta (TestFlight, Internal Testing)

**CI/CD** :
- GitHub Actions
- Fastlane
- Automatisation

**Post-déploiement** :
- Monitoring (Crashlytics, Sentry)
- Analytics
- Mises à jour (OTA, force update)

---

### 7. 📊 [DATA_MODELS_REFERENCE.md](./DATA_MODELS_REFERENCE.md)
**Référence des modèles de données**

Documentation détaillée de tous les modèles backend :

**Modèles** :
- User, CustomerProfile, DriverProfile
- Restaurant, Category, MenuItem, RestaurantReview
- Order, OrderItem
- DeliveryTracking, DeliveryZone, DriverRating
- Coupon, CouponUsage, Promotion

**Pour chaque modèle** :
- Tous les champs avec types et contraintes
- Relations (ForeignKey, ManyToMany, OneToOne)
- Formats JSON (request/response)
- Choix (enums) disponibles
- Exemples complets

**Sections supplémentaires** :
- Diagramme des relations entre modèles
- Formats JSON spécifiques (adresses, horaires, options)
- Workflows (commande, paiement, livraison)
- Règles de validation
- Indexes recommandés
- Conseils d'implémentation mobile

**Utilisez cette référence** pour créer vos interfaces TypeScript et comprendre les données.

---

## Démarrage rapide

### Étape 1 : Configuration de l'environnement

```bash
# Initialiser un nouveau projet React Native
npx react-native init MultiRestaurants --template react-native-template-typescript

cd MultiRestaurants

# Installer les dépendances principales
npm install @reduxjs/toolkit react-redux
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install axios
npm install @react-native-async-storage/async-storage
npm install react-native-dotenv

# Pour iOS
cd ios && pod install && cd ..
```

### Étape 2 : Configurer les variables d'environnement

Créer `.env` :
```bash
API_URL=http://localhost:8000/api/v1
GOOGLE_MAPS_API_KEY_IOS=your_ios_key
GOOGLE_MAPS_API_KEY_ANDROID=your_android_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_key
```

### Étape 3 : Créer la structure de dossiers

```
src/
├── api/              # Services API
├── components/       # Composants réutilisables
├── screens/          # Écrans de l'app
├── navigation/       # Configuration navigation
├── store/            # Redux store et slices
├── hooks/            # Custom hooks
├── utils/            # Utilitaires
├── constants/        # Constantes (couleurs, etc.)
└── types/            # Types TypeScript
```

### Étape 4 : Suivre les guides

1. Lire **MOBILE_DEV_GUIDE.md** pour comprendre l'architecture
2. Consulter **API_COMPLETE_REFERENCE.md** pour les endpoints
3. Copier le code de **CODE_EXAMPLES.md** pour démarrer
4. Suivre **FEATURES_CHECKLIST.md** pour le développement
5. Appliquer **UI_UX_GUIDELINES.md** pour le design
6. Utiliser **DATA_MODELS_REFERENCE.md** comme référence
7. Déployer avec **DEPLOYMENT_GUIDE.md** en fin de projet

---

## Fonctionnalités principales

### Pour les clients 👤

✅ **Découverte**
- Liste des restaurants avec filtres (cuisine, prix, note, délai)
- Recherche par nom ou type de cuisine
- Restaurants à proximité (géolocalisation)
- Restaurants populaires et nouveautés

✅ **Commande**
- Parcourir le menu avec photos
- Personnaliser les articles (options, taille)
- Panier avec calcul automatique
- Application de coupons promo
- Choix de l'adresse de livraison
- Paiement sécurisé (carte, cash)

✅ **Suivi**
- Tracking en temps réel sur carte
- Mises à jour de statut
- Temps estimé d'arrivée
- Contact livreur/restaurant

✅ **Profil**
- Historique des commandes
- Adresses enregistrées
- Restaurants favoris
- Moyens de paiement
- Notifications

### Pour les restaurants 🍴

✅ **Gestion du menu**
- Ajouter/modifier/supprimer des articles
- Upload de photos
- Gérer les catégories
- Prix et disponibilité

✅ **Gestion des commandes**
- Notifications de nouvelles commandes
- Accepter/refuser
- Temps de préparation
- Marquer comme prête

✅ **Analytics**
- Revenus journaliers/mensuels
- Articles populaires
- Avis clients
- Performance

✅ **Promotions**
- Créer des promotions
- Happy hours
- Offres spéciales

### Pour les livreurs 🚴

✅ **Gestion des courses**
- Liste des courses disponibles
- Accepter/refuser
- Navigation GPS
- Marquer comme récupérée/livrée

✅ **Revenus**
- Suivi des gains
- Pourboires
- Historique des livraisons
- Statistiques

✅ **Profil**
- Disponibilité (online/offline)
- Véhicule
- Notes et évaluations

---

## Estimation de développement

### Par module

| Module | Temps estimé | Complexité |
|--------|-------------|------------|
| Configuration initiale | 8h | Moyenne |
| Authentification | 20h | Moyenne |
| Module Client | 60-80h | Élevée |
| Module Restaurant | 30-40h | Moyenne |
| Module Livreur | 25-35h | Moyenne |
| Notifications & Real-time | 15-20h | Élevée |
| Paiements | 15-20h | Élevée |
| Tests | 20-30h | Variable |
| Déploiement | 10-15h | Moyenne |

**Total** : ~150-200 heures pour une v1 complète

### Planning recommandé

**Sprint 1 (2 semaines)** : Setup + Auth + Navigation
**Sprint 2 (2 semaines)** : Module Client (base)
**Sprint 3 (2 semaines)** : Module Client (complet) + Paiement
**Sprint 4 (2 semaines)** : Module Restaurant + Livreur
**Sprint 5 (2 semaines)** : Real-time + Notifications
**Sprint 6 (1 semaine)** : Tests + Bug fixes
**Sprint 7 (1 semaine)** : Déploiement

**Total** : ~12 semaines (3 mois)

---

## Technologies et bibliothèques

### Core

```json
{
  "react": "^18.2.0",
  "react-native": "^0.72.0",
  "typescript": "^5.0.0"
}
```

### State Management

```json
{
  "@reduxjs/toolkit": "^1.9.5",
  "react-redux": "^8.1.1"
}
```

### Navigation

```json
{
  "@react-navigation/native": "^6.1.7",
  "@react-navigation/stack": "^6.3.17",
  "@react-navigation/bottom-tabs": "^6.5.8",
  "react-native-screens": "^3.22.0",
  "react-native-safe-area-context": "^4.6.3"
}
```

### API & Data

```json
{
  "axios": "^1.4.0",
  "@react-native-async-storage/async-storage": "^1.19.0",
  "react-native-dotenv": "^3.4.9"
}
```

### UI Components

```json
{
  "react-native-vector-icons": "^10.0.0",
  "react-native-linear-gradient": "^2.8.0",
  "react-native-modal": "^13.0.1"
}
```

### Maps & Location

```json
{
  "react-native-maps": "^1.7.1",
  "@react-native-community/geolocation": "^3.0.6",
  "react-native-geolocation-service": "^5.3.1"
}
```

### Payment

```json
{
  "@stripe/stripe-react-native": "^0.28.0"
}
```

### Push Notifications

```json
{
  "@react-native-firebase/app": "^18.3.0",
  "@react-native-firebase/messaging": "^18.3.0"
}
```

### Error Tracking & Analytics

```json
{
  "@sentry/react-native": "^5.8.0",
  "@react-native-firebase/analytics": "^18.3.0"
}
```

---

## Backend API

### Base URL
```
Production: https://api.multirestaurants.com/api/v1
Development: http://localhost:8000/api/v1
```

### Documentation interactive
- Swagger UI : `/api/v1/swagger/`
- ReDoc : `/api/v1/redoc/`

### Authentification
Utilise JWT avec access et refresh tokens.

```http
Authorization: Bearer <access_token>
```

### Endpoints principaux

```
Auth:
  POST   /auth/register/
  POST   /auth/login/
  POST   /auth/token/refresh/
  POST   /auth/logout/

Restaurants:
  GET    /restaurants/
  GET    /restaurants/{id}/
  GET    /restaurants/{id}/menu/
  GET    /restaurants/nearby/

Orders:
  POST   /orders/
  GET    /orders/
  GET    /orders/{id}/
  PATCH  /orders/{id}/status/

Delivery:
  GET    /delivery-tracking/{id}/
  PATCH  /delivery-tracking/{id}/location/

Promotions:
  GET    /coupons/
  POST   /coupons/validate/
```

Voir **API_COMPLETE_REFERENCE.md** pour la liste complète.

---

## Tests

### Tests unitaires

```bash
# Avec Jest
npm test

# Avec coverage
npm test -- --coverage
```

### Tests d'intégration

```bash
# Avec Detox
npm run test:e2e:ios
npm run test:e2e:android
```

### Tests manuels

Checklist dans **FEATURES_CHECKLIST.md** section "Tests et qualité".

---

## Déploiement

### iOS

1. Configurer Apple Developer Account
2. Créer App ID et certificats
3. Build avec Xcode
4. Upload sur App Store Connect
5. Soumettre pour révision

Voir **DEPLOYMENT_GUIDE.md** pour les détails.

### Android

1. Générer keystore
2. Build AAB avec Gradle
3. Upload sur Google Play Console
4. Remplir la fiche store
5. Soumettre pour révision

Voir **DEPLOYMENT_GUIDE.md** pour les détails.

---

## Support et ressources

### Documentation officielle

- **React Native** : https://reactnative.dev
- **Redux Toolkit** : https://redux-toolkit.js.org
- **React Navigation** : https://reactnavigation.org
- **Firebase** : https://rnfirebase.io

### Outils recommandés

- **VS Code** avec extensions :
  - ES7+ React/Redux/React-Native snippets
  - Prettier
  - ESLint
  - React Native Tools

- **Debugging** :
  - Reactotron (Redux debugging)
  - Flipper (React Native debugging)

- **Design** :
  - Figma (design d'interface)
  - Adobe XD (prototypage)

---

## Licence et contribution

### Licence
Projet propriétaire - Tous droits réservés

### Contribution

Si vous trouvez des bugs ou avez des suggestions :
1. Documenter le problème clairement
2. Fournir des steps to reproduce
3. Inclure screenshots si UI bug
4. Proposer une solution si possible

---

## Contacts

**Équipe Backend** : backend@multirestaurants.com
**Équipe Mobile** : mobile@multirestaurants.com
**Support** : support@multirestaurants.com

---

## Changelog

### Version 1.0.0 (Initial)
- Documentation complète créée
- 7 guides spécialisés
- Exemples de code prêts à l'emploi
- Checklist de ~150 features
- Guidelines UI/UX complètes

---

## Notes importantes

### Sécurité

⚠️ **Ne jamais commiter** :
- Clés API dans le code
- Tokens d'accès
- Credentials
- Keystores Android

✅ **Utiliser** :
- Variables d'environnement (`.env`)
- Secrets managers (GitHub Secrets, etc.)
- `.gitignore` configuré correctement

### Performance

🚀 **Optimisations recommandées** :
- Lazy loading des images
- Virtualisation des listes (FlatList)
- Memoization des composants (React.memo)
- Debounce pour la recherche
- Cache API (RTK Query)

### Accessibilité

♿ **À implémenter** :
- Labels pour lecteurs d'écran
- Zones tactiles >= 44x44
- Contraste suffisant
- Support du scaling de texte

---

## Prochaines étapes

1. ✅ **Lire MOBILE_DEV_GUIDE.md** - Comprendre l'architecture
2. ✅ **Configurer l'environnement** - Suivre le démarrage rapide
3. ✅ **Implémenter l'auth** - Utiliser CODE_EXAMPLES.md
4. ✅ **Développer par module** - Suivre FEATURES_CHECKLIST.md
5. ✅ **Appliquer le design** - Respecter UI_UX_GUIDELINES.md
6. ✅ **Intégrer l'API** - Consulter API_COMPLETE_REFERENCE.md
7. ✅ **Tester** - Tests unitaires + E2E
8. ✅ **Déployer** - Suivre DEPLOYMENT_GUIDE.md

---

**Bonne chance avec le développement ! 🚀**

Cette documentation a été créée pour vous fournir tout ce dont vous avez besoin pour réussir. N'hésitez pas à vous y référer régulièrement et à l'améliorer au besoin.

---

**Dernière mise à jour** : 2024-02-15
**Version de la documentation** : 1.0.0
**Backend API Version** : 1.0.0
