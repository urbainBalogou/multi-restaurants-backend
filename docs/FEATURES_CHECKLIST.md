# ✅ CHECKLIST COMPLÈTE DES FONCTIONNALITÉS

Cette checklist exhaustive couvre **toutes** les fonctionnalités à implémenter dans l'application mobile.

---

## 🔐 MODULE AUTHENTIFICATION

### Écrans
- [ ] **Splash Screen**
  - [ ] Logo animé
  - [ ] Vérification de l'authentification
  - [ ] Redirection automatique

- [ ] **Onboarding** (première utilisation)
  - [ ] 3-4 slides expliquant l'app
  - [ ] Boutons "Passer" et "Suivant"
  - [ ] Stockage du flag "onboarding_seen"

- [ ] **Écran de connexion**
  - [ ] Input email
  - [ ] Input mot de passe (avec œil pour montrer/cacher)
  - [ ] Bouton "Se connecter"
  - [ ] Lien "Mot de passe oublié"
  - [ ] Lien "S'inscrire"
  - [ ] Validation des champs
  - [ ] Gestion des erreurs API
  - [ ] Loading state

- [ ] **Écran d'inscription**
  - [ ] Input prénom
  - [ ] Input nom
  - [ ] Input email
  - [ ] Input téléphone (avec code pays)
  - [ ] Input mot de passe (avec force indicator)
  - [ ] Input confirmation mot de passe
  - [ ] Sélection du type d'utilisateur (Client/Restaurateur/Livreur)
  - [ ] Checkbox CGU acceptées
  - [ ] Bouton "S'inscrire"
  - [ ] Validation en temps réel
  - [ ] Gestion des erreurs (email existant, etc.)

- [ ] **Mot de passe oublié**
  - [ ] Input email
  - [ ] Bouton "Réinitialiser"
  - [ ] Message de confirmation

### Fonctionnalités
- [ ] **JWT Token Management**
  - [ ] Stockage sécurisé des tokens (AsyncStorage/SecureStore)
  - [ ] Auto-refresh du token avant expiration
  - [ ] Gestion de la déconnexion automatique
  - [ ] Intercepteurs Axios pour token

- [ ] **Persistance de session**
  - [ ] Garder l'utilisateur connecté
  - [ ] Déconnexion manuelle
  - [ ] Nettoyage des données à la déconnexion

---

## 🏠 MODULE CLIENT

### Navigation
- [ ] **Bottom Tab Navigator**
  - [ ] Accueil
  - [ ] Recherche
  - [ ] Commandes
  - [ ] Profil

### Écran Accueil
- [ ] **Header**
  - [ ] Message de bienvenue personnalisé
  - [ ] Localisation actuelle (cliquable)
  - [ ] Bouton notifications

- [ ] **Barre de recherche**
  - [ ] Recherche en temps réel
  - [ ] Icône de recherche
  - [ ] Placeholder dynamique

- [ ] **Catégories (scroll horizontal)**
  - [ ] Images des catégories
  - [ ] Nom de la catégorie
  - [ ] Filtrage par catégorie
  - [ ] Animation de sélection

- [ ] **Section "Restaurants à proximité"**
  - [ ] Carte des restaurants
  - [ ] Liste des restaurants
  - [ ] Distance calculée
  - [ ] Temps de livraison estimé
  - [ ] Tri par distance/note/popularité

- [ ] **Section "Restaurants populaires"**
  - [ ] Top 10 des restaurants
  - [ ] Badge "Populaire"

- [ ] **Section "Promotions"**
  - [ ] Carousel des promotions actives
  - [ ] Image de la promo
  - [ ] Description
  - [ ] CTA vers le restaurant

- [ ] **Pull to refresh**
- [ ] **Infinite scroll / Pagination**

### Écran Détail Restaurant
- [ ] **Header**
  - [ ] Image cover du restaurant
  - [ ] Bouton retour
  - [ ] Bouton favori (cœur)
  - [ ] Bouton partager

- [ ] **Informations restaurant**
  - [ ] Nom
  - [ ] Note moyenne + nombre d'avis
  - [ ] Tags (type de cuisine)
  - [ ] Temps de livraison estimé
  - [ ] Frais de livraison
  - [ ] Seuil livraison gratuite
  - [ ] Adresse
  - [ ] Téléphone (cliquable)
  - [ ] Horaires d'ouverture (expandable)

- [ ] **Menu par catégories**
  - [ ] Sticky header des catégories
  - [ ] Scroll automatique vers catégorie
  - [ ] Liste des plats avec :
    - [ ] Image
    - [ ] Nom
    - [ ] Description
    - [ ] Prix
    - [ ] Badge "Populaire" si applicable
    - [ ] Badge promo si applicable
    - [ ] Icônes allergènes
    - [ ] Calories

- [ ] **Bottom bar sticky**
  - [ ] Nombre d'articles dans le panier
  - [ ] Total du panier
  - [ ] Bouton "Voir le panier"

### Écran Détail Plat (Modal)
- [ ] **Image pleine largeur**
- [ ] **Bouton fermer**
- [ ] **Informations**
  - [ ] Nom
  - [ ] Description
  - [ ] Prix de base
  - [ ] Temps de préparation
  - [ ] Calories
  - [ ] Allergènes

- [ ] **Options/Personnalisations**
  - [ ] Taille (radio buttons)
  - [ ] Suppléments (checkboxes)
  - [ ] Suppression d'ingrédients (checkboxes)
  - [ ] Calcul du prix avec options

- [ ] **Instructions spéciales**
  - [ ] TextArea pour notes

- [ ] **Quantité**
  - [ ] Boutons - / +
  - [ ] Affichage de la quantité

- [ ] **Bouton "Ajouter au panier"**
  - [ ] Prix total affiché
  - [ ] Animation d'ajout

### Écran Panier
- [ ] **Liste des articles**
  - [ ] Image du plat
  - [ ] Nom
  - [ ] Options sélectionnées
  - [ ] Prix unitaire
  - [ ] Quantité (modifiable)
  - [ ] Bouton supprimer
  - [ ] Instructions spéciales

- [ ] **Information restaurant**
  - [ ] Nom
  - [ ] Temps de livraison

- [ ] **Code promo**
  - [ ] Input code
  - [ ] Bouton "Appliquer"
  - [ ] Liste des coupons disponibles
  - [ ] Affichage du coupon appliqué
  - [ ] Bouton retirer le coupon

- [ ] **Récapitulatif**
  - [ ] Sous-total
  - [ ] Frais de livraison
  - [ ] Remise (coupon)
  - [ ] Taxes
  - [ ] **Total** (en gros)

- [ ] **Bouton "Commander"**
  - [ ] Disabled si panier vide
  - [ ] Navigation vers checkout

### Écran Checkout
- [ ] **Adresse de livraison**
  - [ ] Liste des adresses sauvegardées
  - [ ] Bouton "Ajouter une nouvelle adresse"
  - [ ] Modification d'adresse
  - [ ] Instructions de livraison

- [ ] **Sélection adresse avec carte**
  - [ ] Map interactive
  - [ ] Marqueur déplaçable
  - [ ] Autocomplete d'adresse
  - [ ] Bouton "Utiliser ma position actuelle"

- [ ] **Heure de livraison**
  - [ ] "Dès que possible"
  - [ ] "Programmer pour plus tard" (date/heure picker)

- [ ] **Méthode de paiement**
  - [ ] Espèces
  - [ ] Carte bancaire (Stripe)
  - [ ] Paiement mobile (Apple Pay / Google Pay)
  - [ ] Liste des cartes sauvegardées
  - [ ] Bouton "Ajouter une carte"

- [ ] **Récapitulatif final**
  - [ ] Restaurant
  - [ ] Articles
  - [ ] Adresse
  - [ ] Total

- [ ] **Bouton "Confirmer et payer"**
  - [ ] Loading state
  - [ ] Gestion des erreurs
  - [ ] Redirection vers succès

### Écran Confirmation Commande
- [ ] **Animation de succès** (checkmark animé)
- [ ] **Numéro de commande**
- [ ] **Temps estimé de livraison**
- [ ] **Bouton "Suivre ma commande"**
- [ ] **Bouton "Retour à l'accueil"**

### Écran Suivi Commande (Tracking)
- [ ] **Timeline du statut**
  - [ ] Confirmée
  - [ ] En préparation
  - [ ] Prête
  - [ ] En cours de livraison
  - [ ] Livrée

- [ ] **Carte en temps réel**
  - [ ] Position du livreur (marqueur animé)
  - [ ] Position du restaurant
  - [ ] Position du client
  - [ ] Trajet tracé
  - [ ] Mise à jour toutes les 10 secondes

- [ ] **Informations livreur**
  - [ ] Photo
  - [ ] Nom
  - [ ] Note
  - [ ] Véhicule
  - [ ] Bouton appeler
  - [ ] Bouton message

- [ ] **ETA (Estimated Time of Arrival)**
  - [ ] Temps restant
  - [ ] Distance restante

- [ ] **Bouton "Annuler la commande"**
  - [ ] Uniquement si status = pending/confirmed
  - [ ] Confirmation popup

### Écran Historique Commandes
- [ ] **Liste des commandes passées**
  - [ ] Filtre par statut
  - [ ] Tri par date
  - [ ] Card par commande :
    - [ ] Restaurant
    - [ ] Date
    - [ ] Montant
    - [ ] Statut
    - [ ] Bouton "Recommander"
    - [ ] Bouton "Voir détails"

- [ ] **Détail d'une commande passée**
  - [ ] Toutes les infos
  - [ ] Bouton "Renoter restaurant"
  - [ ] Bouton "Noter le livreur"
  - [ ] Bouton "Réclamation"

### Écran Profil Client
- [ ] **Photo de profil**
  - [ ] Upload depuis galerie
  - [ ] Capture photo
  - [ ] Crop image

- [ ] **Informations personnelles**
  - [ ] Nom, prénom
  - [ ] Email
  - [ ] Téléphone
  - [ ] Bouton "Modifier"

- [ ] **Mes adresses**
  - [ ] Liste des adresses
  - [ ] Ajouter/Modifier/Supprimer
  - [ ] Adresse par défaut

- [ ] **Mes cartes de paiement**
  - [ ] Liste des cartes (derniers 4 chiffres)
  - [ ] Ajouter/Supprimer
  - [ ] Carte par défaut

- [ ] **Restaurants favoris**
  - [ ] Liste avec images
  - [ ] Bouton supprimer des favoris

- [ ] **Mes coupons**
  - [ ] Coupons disponibles
  - [ ] Coupons utilisés
  - [ ] Date d'expiration

- [ ] **Historique des commandes** (lien)

- [ ] **Paramètres**
  - [ ] Notifications push (toggle)
  - [ ] Notifications email (toggle)
  - [ ] Notifications SMS (toggle)
  - [ ] Langue
  - [ ] Mode sombre

- [ ] **Support**
  - [ ] FAQ
  - [ ] Contacter le support
  - [ ] À propos

- [ ] **Bouton "Se déconnecter"**
  - [ ] Confirmation popup

---

## 🏪 MODULE RESTAURATEUR

### Dashboard Restaurant
- [ ] **Statistiques**
  - [ ] Revenus du jour
  - [ ] Nombre de commandes
  - [ ] Note moyenne
  - [ ] Graphique des revenus (7 derniers jours)

- [ ] **Commandes en cours**
  - [ ] Liste en temps réel
  - [ ] Notifications sonores
  - [ ] Badge de nouvelles commandes

- [ ] **Toggle "Accepter les commandes"**
  - [ ] Switch ON/OFF
  - [ ] Confirmation popup

### Gestion des Commandes
- [ ] **Liste des commandes**
  - [ ] Filtre par statut
  - [ ] Tri par date
  - [ ] Card par commande :
    - [ ] Numéro
    - [ ] Client (nom, téléphone)
    - [ ] Articles
    - [ ] Montant
    - [ ] Statut
    - [ ] Timer depuis création

- [ ] **Détail commande**
  - [ ] Informations complètes
  - [ ] Boutons d'action selon statut :
    - [ ] Accepter / Refuser (pending)
    - [ ] Marquer "En préparation" (confirmed)
    - [ ] Marquer "Prêt" (preparing)

- [ ] **Notifications**
  - [ ] Push pour nouvelle commande
  - [ ] Son d'alerte
  - [ ] Badge sur l'app

### Gestion du Menu
- [ ] **Liste des plats**
  - [ ] Groupés par catégorie
  - [ ] Drag & drop pour réordonner
  - [ ] Toggle disponibilité ON/OFF
  - [ ] Bouton "Ajouter un plat"

- [ ] **Ajouter/Modifier un plat**
  - [ ] Upload image
  - [ ] Nom
  - [ ] Description
  - [ ] Prix
  - [ ] Catégorie (select)
  - [ ] Temps de préparation
  - [ ] Options/Suppléments (multi)
  - [ ] Allergènes (multi-select)
  - [ ] Calories
  - [ ] Disponibilité

- [ ] **Catégories**
  - [ ] Ajouter/Modifier/Supprimer

### Gestion des Promotions
- [ ] **Liste des promotions**
  - [ ] Actives
  - [ ] À venir
  - [ ] Expirées

- [ ] **Créer une promotion**
  - [ ] Nom
  - [ ] Description
  - [ ] Type (pourcentage / montant fixe / buy X get Y)
  - [ ] Valeur
  - [ ] Articles concernés (multi-select)
  - [ ] Date début / fin
  - [ ] Jours de la semaine
  - [ ] Heures début / fin
  - [ ] Upload image

### Profil Restaurant
- [ ] **Informations**
  - [ ] Nom
  - [ ] Description
  - [ ] Image cover
  - [ ] Logo
  - [ ] Adresse
  - [ ] Téléphone
  - [ ] Email

- [ ] **Horaires d'ouverture**
  - [ ] Par jour de la semaine
  - [ ] Heure ouverture / fermeture
  - [ ] Toggle "Fermé"

- [ ] **Paramètres de livraison**
  - [ ] Frais de livraison
  - [ ] Seuil livraison gratuite
  - [ ] Rayon de livraison (km)
  - [ ] Temps de livraison estimé

- [ ] **Zones de livraison** (optionnel avancé)
  - [ ] Dessiner sur carte
  - [ ] Prix par zone

### Statistiques & Rapports
- [ ] **Revenus**
  - [ ] Par jour/semaine/mois
  - [ ] Graphiques

- [ ] **Commandes**
  - [ ] Nombre total
  - [ ] Taux d'acceptation
  - [ ] Temps moyen de préparation

- [ ] **Plats populaires**
  - [ ] Top 10
  - [ ] Nombre de ventes

- [ ] **Avis clients**
  - [ ] Note moyenne
  - [ ] Évolution
  - [ ] Derniers commentaires

---

## 🚗 MODULE LIVREUR

### Dashboard Livreur
- [ ] **Toggle "Disponible"**
  - [ ] Switch ON/OFF
  - [ ] Indicateur visuel

- [ ] **Statistiques du jour**
  - [ ] Nombre de livraisons
  - [ ] Gains du jour
  - [ ] Pourboires
  - [ ] Note moyenne

- [ ] **Commande en cours**
  - [ ] Si assigné : afficher la commande
  - [ ] Si non : message d'attente

### Livraison Active
- [ ] **Carte plein écran**
  - [ ] Position livreur (GPS temps réel)
  - [ ] Marker restaurant
  - [ ] Marker client
  - [ ] Trajet tracé
  - [ ] Bouton "Centrer sur ma position"

- [ ] **Informations commande** (bottom sheet)
  - [ ] Numéro
  - [ ] Restaurant (nom, adresse, téléphone)
  - [ ] Client (nom, adresse, téléphone)
  - [ ] Articles
  - [ ] Montant
  - [ ] Instructions

- [ ] **Actions selon étape**
  - [ ] "Arrivé au restaurant" (ready → picked_up)
  - [ ] "Commande récupérée" (picked_up → en route)
  - [ ] "Livraison effectuée" (en route → delivered)

- [ ] **Boutons d'appel**
  - [ ] Appeler le restaurant
  - [ ] Appeler le client

- [ ] **Navigation**
  - [ ] Bouton "Ouvrir dans Maps" (Google Maps / Apple Maps)

### Confirmation Livraison
- [ ] **Photo de preuve de livraison** (optionnel)
- [ ] **Signature du client** (optionnel)
- [ ] **Confirmation finale**
- [ ] **Demande de pourboire** (optionnel)

### Historique Livraisons
- [ ] **Liste des livraisons**
  - [ ] Par date
  - [ ] Montant
  - [ ] Pourboire
  - [ ] Distance
  - [ ] Note reçue

- [ ] **Statistiques**
  - [ ] Total gains (semaine/mois)
  - [ ] Nombre de livraisons
  - [ ] Distance totale parcourue
  - [ ] Note moyenne

### Profil Livreur
- [ ] **Photo de profil**
- [ ] **Informations**
  - [ ] Nom, prénom
  - [ ] Téléphone
  - [ ] Email

- [ ] **Véhicule**
  - [ ] Type (vélo/scooter/voiture)
  - [ ] Plaque d'immatriculation

- [ ] **Documents** (upload)
  - [ ] Permis de conduire
  - [ ] Carte grise
  - [ ] Assurance
  - [ ] Casier judiciaire

- [ ] **Paiement**
  - [ ] IBAN pour virements
  - [ ] Historique des paiements

---

## 🔔 MODULE NOTIFICATIONS

### Notifications Push
- [ ] **Configuration Firebase**
  - [ ] iOS setup
  - [ ] Android setup
  - [ ] Obtenir FCM token

- [ ] **Types de notifications**
  - [ ] Nouvelle commande (restaurant)
  - [ ] Commande assignée (livreur)
  - [ ] Changement de statut (client)
  - [ ] Promotion disponible
  - [ ] Message du support

- [ ] **Gestion des permissions**
  - [ ] Demander la permission au démarrage
  - [ ] Gérer le refus

- [ ] **Centre de notifications**
  - [ ] Liste des notifications
  - [ ] Marquer comme lu
  - [ ] Supprimer

### Notifications locales
- [ ] **Rappels**
  - [ ] Commande prête
  - [ ] Livraison proche

---

## 🗺️ MODULE GÉOLOCALISATION

### Fonctionnalités
- [ ] **Obtenir la position actuelle**
  - [ ] Demander permission
  - [ ] Gérer le refus
  - [ ] Gérer l'erreur GPS désactivé

- [ ] **Suivi en temps réel** (livreur)
  - [ ] Update position toutes les 10s
  - [ ] Envoyer au backend

- [ ] **Calcul de distance**
  - [ ] Restaurant → Client
  - [ ] Livreur → Restaurant
  - [ ] Livreur → Client

- [ ] **Recherche d'adresse**
  - [ ] Autocomplete Google Places
  - [ ] Géolocalisation inverse (lat/lng → adresse)

---

## 💳 MODULE PAIEMENT

### Stripe Integration
- [ ] **Configuration**
  - [ ] Publishable key
  - [ ] Payment Intent API

- [ ] **Ajouter une carte**
  - [ ] Formulaire Stripe (PCI compliant)
  - [ ] Validation
  - [ ] Sauvegarder (tokenisation)

- [ ] **Payer**
  - [ ] Sélection méthode
  - [ ] Confirmation
  - [ ] Gestion 3D Secure
  - [ ] Success/Error handling

- [ ] **Apple Pay / Google Pay**
  - [ ] Configuration
  - [ ] Bouton natif
  - [ ] Flow de paiement

---

## 📊 MODULE ANALYTICS

### Tracking Events
- [ ] **Installation**
- [ ] **Inscription**
- [ ] **Connexion**
- [ ] **Consultation restaurant**
- [ ] **Ajout au panier**
- [ ] **Commande créée**
- [ ] **Paiement effectué**
- [ ] **Erreurs**

### Outils
- [ ] Firebase Analytics
- [ ] Mixpanel (optionnel)
- [ ] Sentry (crash reporting)

---

## 🎨 MODULE UI/UX

### Animations
- [ ] **Transitions entre écrans** (React Navigation)
- [ ] **Animations de liste** (FlatList optimisé)
- [ ] **Skeleton loaders**
- [ ] **Pull to refresh** animé
- [ ] **Boutons avec feedback** (scale/opacity)
- [ ] **Modal entrées/sorties**
- [ ] **Ajout au panier** (flying animation)

### Thème
- [ ] **Mode clair** (par défaut)
- [ ] **Mode sombre**
- [ ] **Fichier de couleurs centralisé**
- [ ] **Fichier de typographie**
- [ ] **Fichier de spacing**

### Accessibilité
- [ ] **Tailles de police ajustables**
- [ ] **Labels pour screen readers**
- [ ] **Contraste des couleurs**
- [ ] **Touch targets >= 44px**

---

## 🧪 MODULE TESTS

### Tests unitaires
- [ ] Redux slices
- [ ] Utilitaires
- [ ] Helpers

### Tests d'intégration
- [ ] Services API
- [ ] Flux d'authentification
- [ ] Flux de commande

### Tests E2E
- [ ] Detox setup
- [ ] Parcours complet client
- [ ] Parcours restaurant
- [ ] Parcours livreur

---

## 🚀 MODULE DÉPLOIEMENT

### iOS
- [ ] **Configuration Xcode**
  - [ ] Bundle Identifier
  - [ ] Version / Build number
  - [ ] Signing & Capabilities

- [ ] **App Store Connect**
  - [ ] Créer l'app
  - [ ] Screenshots
  - [ ] Description
  - [ ] Icône

- [ ] **TestFlight**
  - [ ] Build upload
  - [ ] Beta testing

- [ ] **Release**
  - [ ] Soumission App Store
  - [ ] Review

### Android
- [ ] **Configuration Gradle**
  - [ ] Application ID
  - [ ] Version code/name
  - [ ] Signing config

- [ ] **Google Play Console**
  - [ ] Créer l'app
  - [ ] Screenshots
  - [ ] Description
  - [ ] Icône

- [ ] **Release tracks**
  - [ ] Internal testing
  - [ ] Open/Closed beta
  - [ ] Production

---

## 📈 FONCTIONNALITÉS AVANCÉES (Optionnelles)

### Chat en temps réel
- [ ] Client ↔ Restaurant
- [ ] Client ↔ Livreur
- [ ] Firebase Realtime DB / Socket.io

### Programme de fidélité
- [ ] Points par commande
- [ ] Niveaux (Bronze/Argent/Or)
- [ ] Récompenses

### Parrainage
- [ ] Code de parrainage
- [ ] Réduction parrain/filleul

### Abonnement premium
- [ ] Livraison gratuite illimitée
- [ ] Stripe Subscriptions

### Partage social
- [ ] Partager un restaurant
- [ ] Partager une commande
- [ ] Inviter des amis

### IA / Recommandations
- [ ] Suggestions personnalisées
- [ ] "Vous aimerez aussi..."
- [ ] Historique des goûts

---

## ✅ CRITÈRES DE QUALITÉ

- [ ] **Performance**
  - [ ] App < 50MB
  - [ ] Démarrage < 3s
  - [ ] Navigation fluide (60 FPS)
  - [ ] Images optimisées

- [ ] **UX**
  - [ ] Pas d'écran sans feedback
  - [ ] Loading states partout
  - [ ] Messages d'erreur clairs
  - [ ] Confirmations pour actions critiques

- [ ] **Sécurité**
  - [ ] Tokens stockés en sécurisé
  - [ ] HTTPS uniquement
  - [ ] Validation côté client
  - [ ] Pas de données sensibles en clair

- [ ] **Code Quality**
  - [ ] ESLint configuré
  - [ ] Prettier configuré
  - [ ] Pas de console.log en prod
  - [ ] Components réutilisables
  - [ ] Code commenté (fonctions complexes)

---

**Total estimé** : ~150-200 heures de développement pour une app complète et professionnelle.

**Priorisation recommandée** :
1. ⭐️ Authentification
2. ⭐️ Liste restaurants
3. ⭐️ Panier & Commande
4. ⭐️ Tracking
5. ⭐ Profil
6. Notifications
7. Paiement Stripe
8. Modules restaurateur/livreur
9. Fonctionnalités avancées
