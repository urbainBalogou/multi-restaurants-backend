# Guide de Déploiement - Multi-Restaurants Mobile App

## Table des matières
1. [Prérequis](#prérequis)
2. [Configuration des comptes développeurs](#configuration-des-comptes-développeurs)
3. [Configuration du projet](#configuration-du-projet)
4. [Build et signature](#build-et-signature)
5. [Déploiement iOS](#déploiement-ios)
6. [Déploiement Android](#déploiement-android)
7. [Tests Beta](#tests-beta)
8. [Gestion des versions](#gestion-des-versions)
9. [CI/CD](#cicd)
10. [Post-déploiement](#post-déploiement)
11. [Checklist de déploiement](#checklist-de-déploiement)

---

## Prérequis

### Comptes requis
- [ ] Compte Apple Developer (99$/an) - Pour iOS
- [ ] Compte Google Play Developer (25$ unique) - Pour Android
- [ ] Compte Firebase - Pour push notifications et analytics
- [ ] Compte Stripe - Pour les paiements
- [ ] Compte Google Maps Platform - Pour les cartes

### Outils de développement

**Pour iOS** :
- macOS 11.0 ou supérieur
- Xcode 14.0 ou supérieur
- CocoaPods 1.11 ou supérieur
- Fastlane (optionnel mais recommandé)

**Pour Android** :
- Android Studio Arctic Fox ou supérieur
- JDK 11 ou supérieur
- Android SDK (API 33 minimum)
- Gradle 7.5 ou supérieur

**Général** :
- Node.js 18 LTS ou supérieur
- React Native CLI ou Expo CLI
- Git

---

## Configuration des comptes développeurs

### Apple Developer Account

#### 1. Créer le compte
1. Aller sur https://developer.apple.com
2. S'inscrire avec un Apple ID
3. Payer les frais annuels de 99$
4. Attendre l'approbation (24-48h généralement)

#### 2. Créer l'App ID
```bash
# Via Xcode ou sur https://developer.apple.com/account

Bundle ID: com.multirestaurants.app
Description: Multi-Restaurants Food Delivery
Capabilities à activer:
  - Push Notifications
  - In-App Purchase (si nécessaire)
  - Sign in with Apple (si nécessaire)
  - Maps
  - Background Modes (Location updates, Remote notifications)
```

#### 3. Créer les certificats

**Distribution Certificate** :
```bash
# Générer une clé privée
openssl genrsa -out private.key 2048

# Créer une demande de certificat (CSR)
# Ou utiliser Keychain Access > Certificate Assistant > Request a Certificate
```

**Push Notification Certificate** :
- Aller dans Certificates, Identifiers & Profiles
- Créer un certificat APNs (Apple Push Notification service)
- Télécharger et installer dans Keychain

#### 4. Créer les profils de provisioning
- **Development** : Pour tester sur appareils physiques
- **Ad Hoc** : Pour distribution interne
- **App Store** : Pour distribution publique

### Google Play Console

#### 1. Créer le compte
1. Aller sur https://play.google.com/console
2. Créer un compte développeur
3. Payer les frais uniques de 25$
4. Remplir les informations de compte

#### 2. Créer l'application
```
Nom de l'application: Multi-Restaurants
Langue par défaut: Français
Type: Application
Gratuite/Payante: Gratuite (avec achats intégrés si nécessaire)
```

#### 3. Configurer la signature de l'application
```bash
# Générer une clé de signature
keytool -genkeypair -v -storetype PKCS12 \
  -keystore multi-restaurants.keystore \
  -alias multi-restaurants \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000

# Informations à fournir:
# - Mot de passe du keystore
# - Nom, organisation, ville, etc.
```

**IMPORTANT** : Sauvegarder le keystore et le mot de passe en lieu sûr !

#### 4. Configurer Google Play App Signing
- Activer Google Play App Signing
- Télécharger le upload certificate
- Configurer les clés de signature

---

## Configuration du projet

### Variables d'environnement

Créer `.env.production` :
```bash
# API
API_URL=https://api.multirestaurants.com/api/v1

# Firebase
FIREBASE_API_KEY=your_firebase_api_key
FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id

# Google Maps
GOOGLE_MAPS_API_KEY_IOS=your_ios_key
GOOGLE_MAPS_API_KEY_ANDROID=your_android_key

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_your_key

# Sentry (Error tracking)
SENTRY_DSN=https://your_sentry_dsn

# App Version
APP_VERSION=1.0.0
BUILD_NUMBER=1
```

### Configuration iOS

**ios/MultiRestaurants/Info.plist** :
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Multi-Restaurants</string>
    <key>CFBundleIdentifier</key>
    <string>com.multirestaurants.app</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>

    <!-- Permissions -->
    <key>NSLocationWhenInUseUsageDescription</key>
    <string>Nous avons besoin de votre localisation pour trouver les restaurants à proximité</string>
    <key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
    <string>Pour les livreurs : suivre votre position pendant les livraisons</string>
    <key>NSCameraUsageDescription</key>
    <string>Prendre des photos pour votre profil ou confirmer les livraisons</string>
    <key>NSPhotoLibraryUsageDescription</key>
    <string>Choisir une photo depuis votre galerie</string>

    <!-- Background Modes -->
    <key>UIBackgroundModes</key>
    <array>
        <string>location</string>
        <string>remote-notification</string>
    </array>

    <!-- App Transport Security -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
    </dict>
</dict>
</plist>
```

### Configuration Android

**android/app/build.gradle** :
```gradle
android {
    compileSdkVersion 33
    buildToolsVersion "33.0.0"

    defaultConfig {
        applicationId "com.multirestaurants.app"
        minSdkVersion 23
        targetSdkVersion 33
        versionCode 1
        versionName "1.0.0"
        multiDexEnabled true
    }

    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_RELEASE_STORE_FILE')) {
                storeFile file(MYAPP_RELEASE_STORE_FILE)
                storePassword MYAPP_RELEASE_STORE_PASSWORD
                keyAlias MYAPP_RELEASE_KEY_ALIAS
                keyPassword MYAPP_RELEASE_KEY_PASSWORD
            }
        }
    }

    buildTypes {
        debug {
            applicationIdSuffix ".debug"
            debuggable true
        }
        release {
            minifyEnabled true
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            signingConfig signingConfigs.release
        }
    }
}
```

**android/gradle.properties** :
```properties
MYAPP_RELEASE_STORE_FILE=multi-restaurants.keystore
MYAPP_RELEASE_KEY_ALIAS=multi-restaurants
MYAPP_RELEASE_STORE_PASSWORD=***
MYAPP_RELEASE_KEY_PASSWORD=***

# Performance
org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m
org.gradle.parallel=true
org.gradle.configureondemand=true
```

**android/app/src/main/AndroidManifest.xml** :
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.multirestaurants.app">

    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.VIBRATE" />

    <!-- Background location for drivers -->
    <uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />

    <application
        android:name=".MainApplication"
        android:label="@string/app_name"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:allowBackup="false"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="false">

        <!-- Google Maps API Key -->
        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="YOUR_GOOGLE_MAPS_API_KEY"/>

        <activity
            android:name=".MainActivity"
            android:label="@string/app_name"
            android:configChanges="keyboard|keyboardHidden|orientation|screenSize|uiMode"
            android:launchMode="singleTask"
            android:windowSoftInputMode="adjustResize"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

---

## Build et signature

### Build iOS

#### Development Build
```bash
# Installer les dépendances
cd ios
pod install
cd ..

# Build avec Xcode
xcodebuild -workspace ios/MultiRestaurants.xcworkspace \
  -scheme MultiRestaurants \
  -configuration Debug \
  -sdk iphonesimulator \
  -derivedDataPath ios/build

# Ou lancer depuis Xcode
open ios/MultiRestaurants.xcworkspace
# Product > Build (⌘B)
```

#### Production Build
```bash
# Clean
cd ios
xcodebuild clean
cd ..

# Archive
xcodebuild -workspace ios/MultiRestaurants.xcworkspace \
  -scheme MultiRestaurants \
  -configuration Release \
  -archivePath ios/build/MultiRestaurants.xcarchive \
  archive

# Créer IPA
xcodebuild -exportArchive \
  -archivePath ios/build/MultiRestaurants.xcarchive \
  -exportOptionsPlist ios/exportOptions.plist \
  -exportPath ios/build

# Le fichier .ipa sera dans ios/build/
```

**ios/exportOptions.plist** :
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
    <key>compileBitcode</key>
    <true/>
</dict>
</plist>
```

### Build Android

#### Development Build
```bash
# Build Debug APK
cd android
./gradlew assembleDebug

# Le fichier APK sera dans:
# android/app/build/outputs/apk/debug/app-debug.apk

# Installer sur un appareil connecté
adb install app/build/outputs/apk/debug/app-debug.apk
```

#### Production Build
```bash
# Build Release AAB (Android App Bundle - recommandé)
cd android
./gradlew bundleRelease

# Le fichier AAB sera dans:
# android/app/build/outputs/bundle/release/app-release.aab

# Build Release APK (alternative)
./gradlew assembleRelease

# Le fichier APK sera dans:
# android/app/build/outputs/apk/release/app-release.apk
```

### Optimisation des builds

#### Réduire la taille de l'application

**iOS** :
```ruby
# ios/Podfile
post_install do |installer|
  installer.pods_project.targets.each do |target|
    target.build_configurations.each do |config|
      config.build_settings['ENABLE_BITCODE'] = 'YES'
      config.build_settings['DEAD_CODE_STRIPPING'] = 'YES'
    end
  end
end
```

**Android** - **android/app/build.gradle** :
```gradle
android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    // Splits par ABI (génère plusieurs APKs)
    splits {
        abi {
            enable true
            reset()
            include "armeabi-v7a", "arm64-v8a", "x86", "x86_64"
            universalApk true
        }
    }
}
```

---

## Déploiement iOS

### App Store Connect

#### 1. Créer l'application sur App Store Connect
1. Se connecter à https://appstoreconnect.apple.com
2. My Apps > + > New App
3. Remplir les informations :
   - Platform: iOS
   - Name: Multi-Restaurants
   - Primary Language: French
   - Bundle ID: com.multirestaurants.app
   - SKU: unique identifier

#### 2. Préparer les métadonnées

**Informations de base** :
```
Nom: Multi-Restaurants
Sous-titre: Livraison de repas à domicile
Description:
Découvrez Multi-Restaurants, votre nouvelle application de livraison de repas !

🍕 Commandez dans vos restaurants préférés
📍 Livraison rapide à votre porte
💳 Paiement sécurisé
⭐ Notez et commentez vos expériences

Fonctionnalités:
- Parcourez des centaines de restaurants
- Suivez votre commande en temps réel
- Profitez de promotions exclusives
- Sauvegardez vos adresses favorites
- Contactez directement votre livreur

Téléchargez maintenant et savourez !

Mots-clés: food delivery, restaurant, livraison, repas, cuisine
```

**Catégories** :
- Primary: Food & Drink
- Secondary: Lifestyle

**Captures d'écran requises** :
- iPhone 6.7" (1290 x 2796 pixels) - minimum 3, maximum 10
- iPhone 6.5" (1242 x 2688 pixels)
- iPhone 5.5" (1242 x 2208 pixels)
- iPad Pro 12.9" (2048 x 2732 pixels)

**App Preview (vidéo)** :
- Format: .mov, .mp4, .m4v
- Durée: 15-30 secondes
- Résolution: Même que les captures d'écran

#### 3. Configurer les informations de prix et disponibilité
```
Prix: Gratuit
Disponibilité: Tous les pays (ou sélectionner)
Date de sortie: Manuel ou automatique après approbation
```

#### 4. Uploader le build

**Méthode 1: Xcode** :
```bash
# Ouvrir Xcode
open ios/MultiRestaurants.xcworkspace

# Product > Archive
# Attendre la fin de l'archivage

# Window > Organizer
# Sélectionner l'archive > Distribute App
# App Store Connect > Upload
# Signer avec certificat de distribution
```

**Méthode 2: Transporter App** :
```bash
# Télécharger Transporter depuis App Store
# Glisser-déposer le fichier .ipa
# Deliver
```

**Méthode 3: Command Line (altool)** :
```bash
xcrun altool --upload-app \
  --type ios \
  --file "ios/build/MultiRestaurants.ipa" \
  --username "your@email.com" \
  --password "app-specific-password"
```

#### 5. Soumettre pour révision

1. Sélectionner le build uploadé
2. Remplir les informations de révision :
   - Export Compliance: Répondre aux questions sur le chiffrement
   - Content Rights: Confirmer les droits
   - Advertising Identifier: Si vous utilisez des ads
3. Informations de contact pour la révision
4. Notes pour les reviewers :
```
Comptes de test:
- Client: client@test.com / password123
- Restaurant: restaurant@test.com / password123
- Livreur: driver@test.com / password123

Instructions:
1. Se connecter avec un des comptes ci-dessus
2. Pour tester une commande...
[Détailler le flux]
```

5. Soumettre à App Review
6. Attendre l'approbation (24h-48h généralement)

### TestFlight (Tests Beta)

#### Configuration
```bash
# 1. Upload le build (comme pour App Store)

# 2. Dans App Store Connect > TestFlight
# - Sélectionner le build
# - Remplir "What to Test"
# - Ajouter des testeurs internes (jusqu'à 100)
# - Créer des groupes de testeurs externes
```

#### Inviter des testeurs
```
Testeurs internes:
- Membres de votre équipe
- Accès immédiat
- Pas de révision Apple

Testeurs externes:
- Jusqu'à 10,000 testeurs
- Nécessite révision Apple (première fois)
- Invitation par email
```

#### Recueillir les retours
- Les testeurs peuvent envoyer des screenshots et feedbacks
- Consulter les crashs et métriques dans App Store Connect

---

## Déploiement Android

### Google Play Console

#### 1. Créer une nouvelle version

1. Se connecter à https://play.google.com/console
2. Sélectionner l'application
3. Release > Production > Create new release

#### 2. Uploader le bundle AAB

```bash
# Glisser-déposer le fichier app-release.aab
# Ou uploader via Google Play Console
```

#### 3. Remplir les détadails de la version

**Nom de la version** : `1.0.0 (1)`

**Notes de version** :
```
Français:
Première version de Multi-Restaurants !
- Commandez dans vos restaurants préférés
- Suivez votre livraison en temps réel
- Profitez de promotions exclusives

English:
First version of Multi-Restaurants!
- Order from your favorite restaurants
- Track your delivery in real-time
- Enjoy exclusive promotions
```

#### 4. Préparer la fiche du Store

**Description courte** (80 caractères max) :
```
Livraison de repas rapide et facile. Commandez maintenant !
```

**Description complète** (4000 caractères max) :
```
Multi-Restaurants - Votre app de livraison de repas préférée

Découvrez une nouvelle façon de commander vos repas ! Multi-Restaurants vous connecte avec les meilleurs restaurants de votre ville pour une livraison rapide et fiable.

🍔 FONCTIONNALITÉS

• Parcourez des centaines de restaurants
• Filtrez par cuisine, prix, note, temps de livraison
• Consultez les menus et photos des plats
• Personnalisez vos commandes
• Suivez votre livreur en temps réel sur la carte
• Payez en toute sécurité (carte, PayPal, cash)
• Enregistrez vos adresses favorites
• Profitez de coupons et promotions
• Notez et commentez vos expériences

👨‍🍳 POUR LES RESTAURANTS

Gérez facilement vos commandes, menus et promotions depuis l'app.

🚴 POUR LES LIVREURS

Acceptez des courses, naviguez facilement et maximisez vos revenus.

💳 PAIEMENT SÉCURISÉ

Vos informations de paiement sont protégées avec un chiffrement de niveau bancaire.

⭐ SUPPORT CLIENT

Notre équipe est disponible 7j/7 pour vous aider.

📱 TÉLÉCHARGEZ MAINTENANT

Rejoignez des milliers d'utilisateurs satisfaits et commandez votre prochain repas en quelques clics !
```

**Assets graphiques** :

```
Icône de l'application:
- 512 x 512 pixels
- PNG 32 bits
- Pas d'alpha

Feature Graphic (bannière):
- 1024 x 500 pixels
- PNG ou JPEG
- Obligatoire

Captures d'écran:
- Téléphone: minimum 2, recommandé 8
- 7" Tablette: minimum 2 (optionnel)
- 10" Tablette: minimum 2 (optionnel)
- Formats: JPEG ou PNG 24 bits
- Dimensions minimales: 320px
- Dimensions maximales: 3840px
- Ratio: entre 16:9 et 9:16

Vidéo YouTube (optionnel):
- URL d'une vidéo de présentation
```

#### 5. Catégorisation et contenu

```
Catégorie: Applications > Food & Drink
Tags: livraison, restaurant, food delivery, repas

Classification du contenu:
- Questionnaire à remplir
- Définir la note (3+, 12+, 16+, 18+)

Confidentialité:
- Lien vers politique de confidentialité (obligatoire)
- Lien vers conditions d'utilisation

Public cible et contenu:
- Public: Tous les âges
- Annonces: Oui/Non
- Achats intégrés: Si applicable
```

#### 6. Publier

**Test interne** (rapide) :
- Créer une track "Internal testing"
- Ajouter jusqu'à 100 testeurs
- Disponible en quelques minutes

**Test fermé** (alpha/beta) :
- Créer une track "Closed testing"
- Créer des listes de testeurs
- Révision rapide par Google

**Test ouvert** :
- Tout le monde peut rejoindre
- Nombre illimité de testeurs

**Production** :
- Soumettre à révision
- Approbation généralement en quelques heures
- Déploiement progressif possible (5%, 10%, 20%, 50%, 100%)

```bash
# Déploiement progressif recommandé:
Jour 1: 5% des utilisateurs
Jour 2-3: Surveiller les crashs/feedbacks
Jour 4: 20% si tout va bien
Jour 5-6: Surveiller
Jour 7: 50%
Jour 8-9: Surveiller
Jour 10: 100%
```

---

## Tests Beta

### Programme de beta testing

#### Recrutement des bêta-testeurs
```
Profils recherchés:
- Clients réguliers de services de livraison
- Restaurateurs
- Livreurs/coursiers
- Mix de profils techniques et non-techniques
- Différents appareils iOS et Android
- Différentes versions d'OS

Taille recommandée:
- 50-100 testeurs internes
- 500-1000 testeurs externes
```

#### Plan de test
```
Phase 1 (1 semaine): Tests internes
- Équipe de développement
- Tous les flux critiques
- Tous les rôles (client, restaurant, livreur)

Phase 2 (2 semaines): Alpha fermée
- 50 testeurs sélectionnés
- Focus sur l'UX et bugs critiques
- Feedback quotidien

Phase 3 (2 semaines): Beta fermée
- 200-500 testeurs
- Test en conditions réelles
- Feedback hebdomadaire

Phase 4 (1 semaine): Beta ouverte
- Accès public limité
- Monitoring intensif
- Derniers ajustements

Phase 5: Lancement production
```

#### Collecte de feedback

**Outils** :
- TestFlight Feedback (iOS)
- Google Play Console Feedback (Android)
- Firebase Crashlytics (crashs et erreurs)
- Sentry (error tracking)
- Google Analytics / Firebase Analytics (comportement)
- Surveys in-app (UserTesting, SurveyMonkey)

**Métriques à surveiller** :
```
Technique:
- Taux de crash
- ANR (Application Not Responding) - Android
- Temps de chargement
- Consommation batterie
- Utilisation mémoire/CPU
- Taille de l'app

UX:
- Taux de complétion des commandes
- Temps moyen pour passer une commande
- Taux d'abandon du panier
- Taux de rétention (D1, D7, D30)
- NPS (Net Promoter Score)

Business:
- Nombre de commandes
- Panier moyen
- Taux de conversion
- Utilisation des promotions
```

---

## Gestion des versions

### Semantic Versioning

Format: `MAJOR.MINOR.PATCH`

**Exemples** :
```
1.0.0 - Version initiale
1.0.1 - Bug fix mineur
1.1.0 - Nouvelles fonctionnalités (compatible)
2.0.0 - Changements majeurs (breaking changes)
```

### Stratégie de versioning

**Version de l'app** (`versionName` / `CFBundleShortVersionString`) :
- Visible par les utilisateurs
- Sémantique: 1.0.0

**Build number** (`versionCode` / `CFBundleVersion`) :
- Nombre entier incrémental
- Unique pour chaque build
- iOS: Peut être identique pour même version
- Android: Doit toujours augmenter

**Exemple** :
```
Release 1: v1.0.0 (build 1)
Hotfix:    v1.0.1 (build 2)
Feature:   v1.1.0 (build 3)
Hotfix:    v1.1.1 (build 4)
Major:     v2.0.0 (build 5)
```

### Scripts de versioning

**package.json** :
```json
{
  "version": "1.0.0",
  "scripts": {
    "version:patch": "npm version patch && node scripts/sync-version.js",
    "version:minor": "npm version minor && node scripts/sync-version.js",
    "version:major": "npm version major && node scripts/sync-version.js"
  }
}
```

**scripts/sync-version.js** :
```javascript
const fs = require('fs');
const { version } = require('../package.json');

// Sync iOS
const iosInfoPlist = 'ios/MultiRestaurants/Info.plist';
let iosContent = fs.readFileSync(iosInfoPlist, 'utf8');
iosContent = iosContent.replace(
  /<key>CFBundleShortVersionString<\/key>\s*<string>[\d.]+<\/string>/,
  `<key>CFBundleShortVersionString</key>\n\t<string>${version}</string>`
);
fs.writeFileSync(iosInfoPlist, iosContent);

// Sync Android
const androidBuildGradle = 'android/app/build.gradle';
let androidContent = fs.readFileSync(androidBuildGradle, 'utf8');
androidContent = androidContent.replace(
  /versionName "[\d.]+"/,
  `versionName "${version}"`
);
// Auto-increment versionCode
androidContent = androidContent.replace(
  /versionCode (\d+)/,
  (match, code) => `versionCode ${parseInt(code) + 1}`
);
fs.writeFileSync(androidBuildGradle, androidContent);

console.log(`✅ Version synced to ${version}`);
```

### Changelog

**CHANGELOG.md** :
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.1.0] - 2024-02-15
### Added
- Système de promotions et coupons
- Notation des livreurs
- Chat en temps réel

### Fixed
- Correction du calcul des frais de livraison
- Amélioration de la précision GPS

### Changed
- Interface utilisateur améliorée
- Performance de chargement optimisée

## [1.0.1] - 2024-01-20
### Fixed
- Crash au démarrage sur iOS 15
- Problème de paiement avec certaines cartes

## [1.0.0] - 2024-01-10
### Added
- Version initiale
- Commande de repas
- Suivi en temps réel
- Paiement sécurisé
```

---

## CI/CD

### GitHub Actions

**.github/workflows/ios.yml** :
```yaml
name: iOS Build and Deploy

on:
  push:
    branches: [main, develop]
    tags:
      - 'v*'

jobs:
  build:
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Pods
        run: |
          cd ios
          pod install
          cd ..

      - name: Build iOS app
        run: |
          xcodebuild -workspace ios/MultiRestaurants.xcworkspace \
            -scheme MultiRestaurants \
            -configuration Release \
            -archivePath ios/build/MultiRestaurants.xcarchive \
            archive

      - name: Export IPA
        run: |
          xcodebuild -exportArchive \
            -archivePath ios/build/MultiRestaurants.xcarchive \
            -exportOptionsPlist ios/exportOptions.plist \
            -exportPath ios/build

      - name: Upload to TestFlight
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_PASSWORD: ${{ secrets.APPLE_PASSWORD }}
        run: |
          xcrun altool --upload-app \
            --type ios \
            --file "ios/build/MultiRestaurants.ipa" \
            --username "$APPLE_ID" \
            --password "$APPLE_PASSWORD"

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: ios-ipa
          path: ios/build/*.ipa
```

**.github/workflows/android.yml** :
```yaml
name: Android Build and Deploy

on:
  push:
    branches: [main, develop]
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'

      - name: Setup JDK
        uses: actions/setup-java@v3
        with:
          java-version: '11'
          distribution: 'adopt'

      - name: Install dependencies
        run: npm ci

      - name: Cache Gradle packages
        uses: actions/cache@v3
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}

      - name: Decode Keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.KEYSTORE_BASE64 }}
        run: |
          echo $KEYSTORE_BASE64 | base64 -d > android/app/multi-restaurants.keystore

      - name: Build Android App Bundle
        env:
          MYAPP_RELEASE_STORE_PASSWORD: ${{ secrets.RELEASE_STORE_PASSWORD }}
          MYAPP_RELEASE_KEY_PASSWORD: ${{ secrets.RELEASE_KEY_PASSWORD }}
        run: |
          cd android
          ./gradlew bundleRelease

      - name: Upload to Google Play
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.GOOGLE_PLAY_SERVICE_ACCOUNT }}
          packageName: com.multirestaurants.app
          releaseFiles: android/app/build/outputs/bundle/release/app-release.aab
          track: internal
          status: completed

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: android-aab
          path: android/app/build/outputs/bundle/release/*.aab
```

### Fastlane (recommandé)

**Fastfile** (iOS et Android) :
```ruby
# Fastlane configuration
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "ios/MultiRestaurants.xcodeproj")
    build_app(
      workspace: "ios/MultiRestaurants.xcworkspace",
      scheme: "MultiRestaurants"
    )
    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )
  end

  desc "Deploy to App Store"
  lane :release do
    increment_version_number
    build_app(
      workspace: "ios/MultiRestaurants.xcworkspace",
      scheme: "MultiRestaurants"
    )
    upload_to_app_store(
      force: true,
      submit_for_review: true,
      automatic_release: false,
      submission_information: {
        add_id_info_uses_idfa: false
      }
    )
  end
end

platform :android do
  desc "Deploy a new version to the Google Play (internal testing)"
  lane :internal do
    gradle(
      task: "bundle",
      build_type: "Release",
      project_dir: "android/"
    )
    upload_to_play_store(
      track: 'internal',
      aab: 'android/app/build/outputs/bundle/release/app-release.aab'
    )
  end

  desc "Deploy to Google Play Store"
  lane :release do
    gradle(
      task: "bundle",
      build_type: "Release",
      project_dir: "android/"
    )
    upload_to_play_store(
      track: 'production',
      aab: 'android/app/build/outputs/bundle/release/app-release.aab',
      rollout: '0.1' # Déploiement progressif à 10%
    )
  end
end
```

**Installation** :
```bash
# Installer Fastlane
gem install fastlane

# Initialiser
cd ios && fastlane init
cd android && fastlane init

# Utilisation
fastlane ios beta
fastlane android internal
```

---

## Post-déploiement

### Monitoring

#### Crashlytics / Firebase
```javascript
// Initialisation
import crashlytics from '@react-native-firebase/crashlytics';

// Log custom errors
crashlytics().log('User made purchase');
crashlytics().recordError(new Error('Test error'));

// Set user
crashlytics().setUserId(user.id.toString());
crashlytics().setAttribute('role', user.role);
```

#### Sentry
```javascript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'YOUR_SENTRY_DSN',
  environment: __DEV__ ? 'development' : 'production',
  tracesSampleRate: 1.0,
});

// Capture errors
Sentry.captureException(error);

// Performance monitoring
const transaction = Sentry.startTransaction({
  name: 'checkoutFlow',
});
```

### Analytics

```javascript
import analytics from '@react-native-firebase/analytics';

// Log events
await analytics().logEvent('add_to_cart', {
  item_id: menuItem.id,
  item_name: menuItem.name,
  price: menuItem.price,
});

await analytics().logPurchase({
  value: order.total,
  currency: 'EUR',
  items: order.items,
});

// Set user properties
await analytics().setUserProperty('role', 'customer');
await analytics().setUserId(user.id.toString());
```

### Métriques clés à surveiller

**Stabilité** :
- Crash-free rate (objectif: > 99.5%)
- ANR rate Android (objectif: < 0.5%)
- Temps de démarrage (objectif: < 3s)

**Performance** :
- API response time
- Screen load time
- FPS (objectif: 60 fps)

**Engagement** :
- DAU / MAU
- Session length
- Retention D1, D7, D30
- Taux de conversion

**Business** :
- Nombre de commandes
- GMV (Gross Merchandise Value)
- Panier moyen
- Taux d'annulation

### Gestion des incidents

**Processus** :
```
1. Détection
   - Alertes automatiques (crashs, erreurs API)
   - Rapports utilisateurs
   - Monitoring actif

2. Triage
   - Évaluer la sévérité
   - Identifier l'impact
   - Assigner la priorité

3. Investigation
   - Reproduire le problème
   - Analyser les logs
   - Identifier la cause racine

4. Correction
   - Développer le fix
   - Tester en profondeur
   - Déployer (hotfix si critique)

5. Communication
   - Informer les utilisateurs
   - Mettre à jour le statut
   - Post-mortem
```

**Sévérité** :
- **P0 (Critique)** : App crash, paiements bloqués → Fix immédiat
- **P1 (Majeur)** : Fonctionnalité principale cassée → Fix sous 24h
- **P2 (Moyen)** : Bug gênant → Fix dans prochaine version
- **P3 (Mineur)** : Problème cosmétique → Backlog

### Mises à jour

**Stratégie de release** :
```
Releases majeures: Tous les 2-3 mois
Releases mineures: Toutes les 2-3 semaines
Hotfixes: Si nécessaire (< 24h)
```

**Over-the-Air Updates (OTA)** :
```javascript
// Avec CodePush ou Expo Updates
// Pour mises à jour JavaScript sans passer par les stores

import CodePush from 'react-native-code-push';

const App = () => {
  // Check for updates on start
  useEffect(() => {
    CodePush.sync({
      updateDialog: true,
      installMode: CodePush.InstallMode.ON_NEXT_RESTART,
    });
  }, []);

  return <AppContent />;
};

export default CodePush(App);
```

**Force Update** :
```javascript
// Vérifier la version minimum requise
const checkAppVersion = async () => {
  const response = await api.get('/app-version');
  const { minimumVersion, currentVersion } = response.data;

  if (compareVersions(APP_VERSION, minimumVersion) < 0) {
    // Show force update dialog
    Alert.alert(
      'Mise à jour requise',
      'Une nouvelle version est disponible. Veuillez mettre à jour pour continuer.',
      [
        {
          text: 'Mettre à jour',
          onPress: () => {
            const storeUrl = Platform.select({
              ios: 'https://apps.apple.com/app/id1234567890',
              android: 'https://play.google.com/store/apps/details?id=com.multirestaurants.app',
            });
            Linking.openURL(storeUrl);
          },
        },
      ],
      { cancelable: false }
    );
  }
};
```

---

## Checklist de déploiement

### Pré-déploiement

#### Code et tests
- [ ] Tous les tests passent (unit, integration, E2E)
- [ ] Code review complété
- [ ] Pas de console.log / debugger
- [ ] Pas de TODOs critiques
- [ ] Performance optimisée (pas de memory leaks)
- [ ] Sécurité validée (pas de secrets hardcodés)

#### Configuration
- [ ] Variables d'environnement production configurées
- [ ] API endpoints pointent vers production
- [ ] Clés API production configurées (Google Maps, Stripe, etc.)
- [ ] Firebase projet production configuré
- [ ] Sentry/Crashlytics configuré
- [ ] Analytics configuré

#### Assets
- [ ] Toutes les images optimisées
- [ ] Icônes de l'app créées (toutes les tailles)
- [ ] Splash screen créé
- [ ] Captures d'écran stores préparées
- [ ] Vidéo démo enregistrée (optionnel)

#### Légal
- [ ] Politique de confidentialité publiée
- [ ] Conditions d'utilisation publiées
- [ ] RGPD compliant (si EU)
- [ ] Mentions légales

### iOS

#### Configuration
- [ ] Bundle ID configuré
- [ ] Certificats de distribution créés
- [ ] Profils de provisioning créés
- [ ] Info.plist complété (permissions, etc.)
- [ ] Version et build number incrémentés

#### App Store Connect
- [ ] Application créée sur App Store Connect
- [ ] Métadonnées complétées
- [ ] Captures d'écran uploadées
- [ ] Description et mots-clés optimisés
- [ ] Catégories sélectionnées
- [ ] Prix et disponibilité configurés
- [ ] Classification du contenu complétée

#### Build
- [ ] Build en mode Release
- [ ] Archive créée avec succès
- [ ] IPA uploadé sur App Store Connect
- [ ] Build visible dans TestFlight
- [ ] Tests TestFlight réussis

#### Soumission
- [ ] Build sélectionné pour la version
- [ ] Informations de révision complétées
- [ ] Comptes de test fournis
- [ ] Notes pour reviewers rédigées
- [ ] Soumis pour révision

### Android

#### Configuration
- [ ] applicationId configuré
- [ ] Keystore créé et sauvegardé
- [ ] build.gradle configuré (signing, minify)
- [ ] AndroidManifest.xml complété (permissions)
- [ ] versionCode et versionName incrémentés

#### Google Play Console
- [ ] Application créée
- [ ] Fiche du store complétée
- [ ] Captures d'écran uploadées
- [ ] Description optimisée
- [ ] Catégorie et tags configurés
- [ ] Classification du contenu complétée
- [ ] Politique de confidentialité liée

#### Build
- [ ] Build en mode Release
- [ ] AAB généré avec succès
- [ ] AAB signé avec keystore release
- [ ] Tests de l'AAB réussis

#### Soumission
- [ ] AAB uploadé
- [ ] Notes de version complétées
- [ ] Track sélectionné (internal/alpha/beta/production)
- [ ] Déploiement progressif configuré (si production)
- [ ] Soumis pour révision

### Post-déploiement

#### Monitoring (Première semaine)
- [ ] Crashlytics/Sentry configuré et monitored
- [ ] Analytics configuré et tracké
- [ ] Métriques de performance surveillées
- [ ] Feedback utilisateurs lu quotidiennement
- [ ] Évaluations/notes surveillées

#### Communication
- [ ] Annonce sur réseaux sociaux
- [ ] Email aux utilisateurs existants (si applicable)
- [ ] Communiqué de presse (si applicable)
- [ ] Blog post publié

#### Support
- [ ] Équipe support briefée
- [ ] FAQ mise à jour
- [ ] Canaux de support actifs (email, chat, etc.)

---

## Ressources

### Documentation officielle
- **Apple Developer** : https://developer.apple.com/documentation/
- **Google Play Console** : https://support.google.com/googleplay/android-developer
- **React Native** : https://reactnative.dev/docs/getting-started
- **Fastlane** : https://docs.fastlane.tools/

### Outils
- **Fastlane** : Automatisation des builds et déploiements
- **CodePush** : Mises à jour OTA
- **Sentry** : Error tracking
- **Firebase** : Analytics, Crashlytics, Push notifications
- **Bitrise / CircleCI / GitHub Actions** : CI/CD

### Guides et tutoriels
- **Publishing to Apple App Store** : https://reactnative.dev/docs/publishing-to-app-store
- **Publishing to Google Play Store** : https://reactnative.dev/docs/signed-apk-android
- **App Store Review Guidelines** : https://developer.apple.com/app-store/review/guidelines/
- **Google Play Policy** : https://play.google.com/about/developer-content-policy/

---

## Conclusion

Le déploiement d'une application mobile est un processus complexe qui nécessite une préparation minutieuse. En suivant ce guide et en utilisant les checklists fournies, vous devriez pouvoir déployer l'application Multi-Restaurants avec succès sur l'App Store et Google Play.

**Points clés à retenir** :
1. Préparer tous les assets et métadonnées avant de commencer
2. Tester en profondeur avec TestFlight et tests internes Google Play
3. Utiliser le déploiement progressif pour minimiser les risques
4. Monitorer activement après le lancement
5. Être réactif aux feedbacks et bugs

Bonne chance avec votre lancement ! 🚀
