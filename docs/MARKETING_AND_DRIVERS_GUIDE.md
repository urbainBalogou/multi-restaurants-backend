# Guide Marketing et Gestion des Livreurs - Multi-Restaurants

## Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Gestion des Livreurs par les Restaurants](#gestion-des-livreurs-par-les-restaurants)
3. [Système de Marketing et Publicité](#système-de-marketing-et-publicité)
4. [API Endpoints](#api-endpoints)
5. [Exemples d'utilisation Mobile](#exemples-dutilisation-mobile)
6. [Modèles de données](#modèles-de-données)

---

## Vue d'ensemble

Deux nouvelles fonctionnalités majeures ont été ajoutées à la plateforme Multi-Restaurants :

### 1. **Gestion des Livreurs par les Restaurants**
Les restaurants peuvent désormais créer et gérer leurs propres livreurs, en plus des livreurs indépendants.

### 2. **Système de Marketing et Publicité**
Les restaurants peuvent promouvoir leurs services via différents canaux :
- Publicités dans l'application
- Partage sur réseaux sociaux (WhatsApp, Facebook, Instagram)
- Notifications push ciblées
- Newsletters

---

## Gestion des Livreurs par les Restaurants

### Concept

Les livreurs peuvent être de deux types :
- **Livreurs indépendants** : Ne sont rattachés à aucun restaurant spécifique
- **Livreurs gérés par restaurant** : Sont créés et gérés par un restaurant particulier

### Modèle DriverProfile Étendu

```python
class DriverProfile(models.Model):
    # Nouveau champ : Restaurant qui gère ce livreur
    managed_by_restaurant = ForeignKey(Restaurant, null=True, blank=True)
    
    # Nouveau : Statut du livreur
    status = CharField(choices=['pending', 'approved', 'rejected', 'suspended'])
    
    # Documents pour vérification
    driver_license_number = CharField()
    driver_license_photo = ImageField()
    id_card_photo = ImageField()
    vehicle_insurance = ImageField()
    
    # Nouveaux champs pour revenus et performance
    total_earnings = DecimalField()
    max_delivery_distance_km = FloatField()
    preferred_zones = JSONField()
    availability_schedule = JSONField()
```

### Statuts des Livreurs

| Statut | Description |
|--------|-------------|
| `pending` | En attente d'approbation |
| `approved` | Approuvé et peut effectuer des livraisons |
| `rejected` | Candidature rejetée |
| `suspended` | Suspendu temporairement |

### Workflow de Création d'un Livreur

```
1. Restaurant crée un compte livreur
   ↓
2. Statut initial: 'approved' (direct)
   ↓
3. Livreur reçoit ses identifiants
   ↓
4. Livreur complète son profil (documents, etc.)
   ↓
5. Livreur peut commencer à livrer
```

---

## Système de Marketing et Publicité

### 1. Publicités dans l'Application

#### Types de Publicités

- **banner** : Bannière dans l'app
- **featured** : Restaurant mis en avant
- **promotion** : Promotion spéciale
- **sponsored** : Résultat sponsorisé

#### Modèle RestaurantAdvertisement

```python
{
  "id": 1,
  "restaurant": 12,
  "ad_type": "featured",
  "title": "Burger Week!",
  "description": "Tous nos burgers à -20%",
  "image": "https://...",
  "target_cities": ["Paris", "Lyon"],
  "target_age_min": 18,
  "target_age_max": 35,
  "start_date": "2024-03-01T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "status": "active",
  "budget": 500.00,
  "cost_per_click": 0.50,
  "impressions": 12500,
  "clicks": 850,
  "conversions": 120,
  "click_through_rate": 6.8,
  "conversion_rate": 14.1
}
```

### 2. Partage sur Réseaux Sociaux

#### Plateformes Supportées

- WhatsApp
- Facebook
- Instagram
- Twitter
- Dans l'application

#### Exemple de Partage WhatsApp

**Request** :
```json
POST /api/v1/marketing/shares/quick_share/

{
  "platform": "whatsapp",
  "share_type": "restaurant",
  "restaurant_id": 12,
  "custom_message": "Venez découvrir notre nouveau menu !"
}
```

**Response** :
```json
{
  "id": 45,
  "platform": "whatsapp",
  "share_url": "https://app.multirestaurants.com/restaurant/12",
  "title": "Découvrez Burger King",
  "message": "Venez découvrir notre nouveau menu !",
  "image_url": "https://api.example.com/media/restaurants/burger-king.jpg",
  "whatsapp_url": "https://wa.me/?text=Découvrez%20Burger%20King%0A%0AVenez%20découvrir%20notre%20nouveau%20menu%20!%0A%0Ahttps://app.multirestaurants.com/restaurant/12"
}
```

#### Partager un Article du Menu

```json
POST /api/v1/marketing/shares/quick_share/

{
  "platform": "facebook",
  "share_type": "menu_item",
  "restaurant_id": 12,
  "menu_item_id": 45,
  "custom_message": "J'ai adoré ce burger ! 🍔"
}
```

#### Templates de Partage Personnalisables

Les restaurants peuvent créer des templates réutilisables :

```json
{
  "name": "Nouveau Plat Template",
  "platform": "whatsapp",
  "title_template": "Nouveau : {item_name} chez {restaurant_name}",
  "message_template": "Découvrez notre nouveau plat {item_name} à seulement {price}€ ! Commandez maintenant sur {restaurant_name}. {address}",
  "hashtags": ["foodie", "paris", "burgers"]
}
```

### 3. Notifications Push Ciblées

#### Ciblage

Les restaurants peuvent cibler :
- **Tous les clients** de la zone
- **Clients ayant mis en favori** le restaurant
- **Clients ayant déjà commandé** dans le restaurant

#### Exemple de Campagne

```json
{
  "title": "Happy Hour! 🎉",
  "message": "20% sur tous les burgers de 17h à 19h aujourd'hui!",
  "target_favorites": true,
  "target_previous_orders": true,
  "scheduled_at": "2024-03-15T16:00:00Z",
  "action_type": "menu",
  "action_data": {
    "restaurant_id": 12
  }
}
```

### 4. Newsletters

Les clients peuvent s'abonner aux newsletters des restaurants pour recevoir :
- Nouveaux articles au menu
- Promotions exclusives
- Événements spéciaux

---

## API Endpoints

### Gestion des Livreurs

#### Créer un Livreur (Restaurant uniquement)

```http
POST /api/auth/drivers/
Authorization: Bearer <restaurant_token>

{
  "username": "driver.jean",
  "email": "jean@example.com",
  "password": "securepass123",
  "first_name": "Jean",
  "last_name": "Martin",
  "phone_number": "+33612345678",
  "vehicle_type": "scooter",
  "license_plate": "AB-123-CD",
  "driver_license_number": "1234567890"
}
```

**Response** :
```json
{
  "id": 5,
  "user": {
    "id": 25,
    "username": "driver.jean",
    "email": "jean@example.com",
    "first_name": "Jean",
    "last_name": "Martin",
    "phone_number": "+33612345678",
    "user_type": "driver"
  },
  "managed_by_restaurant": 12,
  "restaurant_name": "Burger King",
  "vehicle_type": "scooter",
  "license_plate": "AB-123-CD",
  "status": "approved",
  "is_available": false,
  "is_independent": false
}
```

#### Lister les Livreurs du Restaurant

```http
GET /api/auth/drivers/?restaurant_id=12
Authorization: Bearer <restaurant_token>
```

#### Mettre à Jour la Disponibilité (Livreur ou Restaurant)

```http
PATCH /api/auth/drivers/5/update_availability/
Authorization: Bearer <driver_token>

{
  "is_available": true
}
```

#### Mettre à Jour la Position (Livreur uniquement)

```http
PATCH /api/auth/drivers/5/update_location/
Authorization: Bearer <driver_token>

{
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

#### Approuver/Rejeter/Suspendre un Livreur

```http
POST /api/auth/drivers/5/approve/
POST /api/auth/drivers/5/reject/
POST /api/auth/drivers/5/suspend/
Authorization: Bearer <restaurant_token>
```

#### Obtenir les Livreurs Disponibles

```http
GET /api/auth/drivers/available_drivers/?latitude=48.8566&longitude=2.3522
Authorization: Bearer <token>
```

#### Statistiques d'un Livreur

```http
GET /api/auth/drivers/5/statistics/
Authorization: Bearer <driver_or_restaurant_token>
```

**Response** :
```json
{
  "total_deliveries": 423,
  "average_rating": 4.7,
  "total_ratings": 156,
  "total_tips": 287.50,
  "total_earnings": 3456.80,
  "last_30_days": {
    "deliveries": 45,
    "earnings": 456.50,
    "average_delivery_time": null
  },
  "current_status": "approved",
  "is_available": true,
  "vehicle_type": "scooter"
}
```

---

### Marketing et Publicité

#### Créer une Publicité

```http
POST /api/v1/marketing/advertisements/
Authorization: Bearer <restaurant_token>

{
  "restaurant": 12,
  "ad_type": "featured",
  "title": "Burger Week",
  "description": "Tous nos burgers à -20%",
  "target_cities": ["Paris", "Lyon"],
  "start_date": "2024-03-01T00:00:00Z",
  "end_date": "2024-03-31T23:59:59Z",
  "budget": 500.00,
  "cost_per_click": 0.50
}
```

#### Obtenir les Publicités Actives

```http
GET /api/v1/marketing/advertisements/active_ads/?city=Paris
```

#### Enregistrer une Impression/Clic/Conversion

```http
POST /api/v1/marketing/advertisements/1/record_impression/
POST /api/v1/marketing/advertisements/1/record_click/
POST /api/v1/marketing/advertisements/1/record_conversion/
```

#### Partage Rapide

```http
POST /api/v1/marketing/shares/quick_share/

{
  "platform": "whatsapp",
  "share_type": "restaurant",
  "restaurant_id": 12,
  "custom_message": "Découvrez ce super restaurant !"
}
```

#### Statistiques de Partage

```http
GET /api/v1/marketing/shares/analytics/?restaurant_id=12
Authorization: Bearer <restaurant_token>
```

**Response** :
```json
{
  "total_shares": 450,
  "total_views": 8500,
  "total_clicks": 1200,
  "conversion_rate": 14.1,
  "by_platform": {
    "whatsapp": {"count": 200, "views": 4000, "clicks": 600},
    "facebook": {"count": 150, "views": 3000, "clicks": 400},
    "instagram": {"count": 100, "views": 1500, "clicks": 200}
  },
  "by_type": {
    "restaurant": {"count": 250, "views": 5000, "clicks": 700},
    "menu_item": {"count": 150, "views": 2500, "clicks": 400},
    "promotion": {"count": 50, "views": 1000, "clicks": 100}
  }
}
```

#### S'abonner à la Newsletter

```http
POST /api/v1/marketing/newsletter-subscriptions/subscribe/
Authorization: Bearer <customer_token>

{
  "restaurant_id": 12
}
```

#### Créer une Campagne Push

```http
POST /api/v1/marketing/push-campaigns/
Authorization: Bearer <restaurant_token>

{
  "restaurant": 12,
  "title": "Happy Hour! 🎉",
  "message": "20% sur tous les burgers de 17h à 19h!",
  "target_favorites": true,
  "target_previous_orders": true,
  "scheduled_at": "2024-03-15T16:00:00Z",
  "action_type": "menu"
}
```

#### Envoyer la Campagne Immédiatement

```http
POST /api/v1/marketing/push-campaigns/1/send_now/
Authorization: Bearer <restaurant_token>
```

---

## Exemples d'utilisation Mobile

### 1. Interface Restaurant : Gérer les Livreurs

#### Écran : Liste des Livreurs

```typescript
// Récupérer les livreurs du restaurant
const { data: drivers, isLoading } = useGetDriversQuery({
  restaurant_id: restaurantId,
});

// Affichage
<FlatList
  data={drivers}
  renderItem={({ item }) => (
    <DriverCard
      driver={item}
      onApprove={() => approveDriver(item.id)}
      onSuspend={() => suspendDriver(item.id)}
    />
  )}
/>
```

#### Créer un Nouveau Livreur

```typescript
const [createDriver] = useCreateDriverMutation();

const handleCreateDriver = async (driverData) => {
  try {
    const result = await createDriver({
      username: driverData.username,
      email: driverData.email,
      password: driverData.password,
      first_name: driverData.firstName,
      last_name: driverData.lastName,
      phone_number: driverData.phone,
      vehicle_type: driverData.vehicleType,
      license_plate: driverData.licensePlate,
    }).unwrap();
    
    Alert.alert('Succès', 'Livreur créé avec succès!');
  } catch (error) {
    Alert.alert('Erreur', error.message);
  }
};
```

### 2. Interface Livreur : Disponibilité et Position

#### Mettre à Jour la Disponibilité

```typescript
const [updateAvailability] = useUpdateDriverAvailabilityMutation();

const toggleAvailability = async (isAvailable) => {
  try {
    await updateAvailability({
      driverId: currentDriver.id,
      is_available: isAvailable,
    }).unwrap();
    
    setIsAvailable(isAvailable);
  } catch (error) {
    Alert.alert('Erreur', error.message);
  }
};
```

#### Suivre la Position en Temps Réel

```typescript
useEffect(() => {
  const watchId = Geolocation.watchPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;
      
      // Mettre à jour la position sur le serveur
      await updateDriverLocation({
        driverId: currentDriver.id,
        latitude,
        longitude,
      });
    },
    (error) => console.error(error),
    {
      enableHighAccuracy: true,
      distanceFilter: 50, // Mettre à jour tous les 50 mètres
      interval: 10000, // Ou toutes les 10 secondes
    }
  );
  
  return () => Geolocation.clearWatch(watchId);
}, []);
```

### 3. Interface Restaurant : Marketing

#### Partager le Restaurant sur WhatsApp

```typescript
const [quickShare] = useQuickShareMutation();

const shareOnWhatsApp = async () => {
  try {
    const result = await quickShare({
      platform: 'whatsapp',
      share_type: 'restaurant',
      restaurant_id: restaurantId,
      custom_message: 'Découvrez notre restaurant!',
    }).unwrap();
    
    // Ouvrir WhatsApp avec le message pré-rempli
    Linking.openURL(result.whatsapp_url);
  } catch (error) {
    Alert.alert('Erreur', error.message);
  }
};
```

#### Créer une Campagne de Notification Push

```typescript
const [createPushCampaign] = useCreatePushCampaignMutation();

const handleCreateCampaign = async (campaignData) => {
  try {
    const result = await createPushCampaign({
      restaurant: restaurantId,
      title: campaignData.title,
      message: campaignData.message,
      target_favorites: campaignData.targetFavorites,
      target_previous_orders: campaignData.targetPreviousOrders,
      scheduled_at: campaignData.scheduledAt,
      action_type: 'menu',
    }).unwrap();
    
    Alert.alert('Succès', 'Campagne créée!');
  } catch (error) {
    Alert.alert('Erreur', error.message);
  }
};
```

#### Voir les Statistiques de Marketing

```typescript
const { data: analytics } = useGetShareAnalyticsQuery({
  restaurant_id: restaurantId,
});

// Affichage
<View>
  <Text>Total de partages : {analytics.total_shares}</Text>
  <Text>Vues totales : {analytics.total_views}</Text>
  <Text>Clics totaux : {analytics.total_clicks}</Text>
  <Text>Taux de conversion : {analytics.conversion_rate}%</Text>
  
  <Text style={{marginTop: 20}}>Par plateforme:</Text>
  {Object.entries(analytics.by_platform).map(([platform, stats]) => (
    <Text key={platform}>
      {platform}: {stats.count} partages, {stats.views} vues
    </Text>
  ))}
</View>
```

### 4. Interface Client : Partager et S'abonner

#### Partager un Restaurant Préféré

```typescript
const ShareButton = ({ restaurant }) => {
  const [quickShare] = useQuickShareMutation();
  
  const shareRestaurant = async (platform) => {
    try {
      const result = await quickShare({
        platform,
        share_type: 'restaurant',
        restaurant_id: restaurant.id,
      }).unwrap();
      
      if (platform === 'whatsapp') {
        Linking.openURL(result.whatsapp_url);
      } else if (platform === 'facebook') {
        Linking.openURL(result.facebook_url);
      }
    } catch (error) {
      Alert.alert('Erreur', error.message);
    }
  };
  
  return (
    <View style={styles.shareButtons}>
      <TouchableOpacity onPress={() => shareRestaurant('whatsapp')}>
        <Icon name="whatsapp" size={32} color="#25D366" />
      </TouchableOpacity>
      <TouchableOpacity onPress={() => shareRestaurant('facebook')}>
        <Icon name="facebook" size={32} color="#1877F2" />
      </TouchableOpacity>
    </View>
  );
};
```

#### S'abonner à la Newsletter

```typescript
const [subscribe] = useSubscribeToNewsletterMutation();

const handleSubscribe = async () => {
  try {
    await subscribe({ restaurant_id: restaurantId }).unwrap();
    Alert.alert('Succès', 'Vous êtes abonné à la newsletter!');
  } catch (error) {
    Alert.alert('Erreur', error.message);
  }
};
```

---

## Modèles de données

### DriverProfile (Étendu)

```typescript
interface DriverProfile {
  id: number;
  user: User;
  managed_by_restaurant: number | null;
  restaurant_name: string | null;
  vehicle_type: 'bike' | 'scooter' | 'car';
  license_plate: string;
  status: 'pending' | 'approved' | 'rejected' | 'suspended';
  is_available: boolean;
  current_latitude: number | null;
  current_longitude: number | null;
  driver_license_number: string;
  driver_license_photo: string;
  id_card_photo: string;
  vehicle_insurance: string;
  average_rating: number;
  total_ratings: number;
  total_deliveries: number;
  total_tips: number;
  total_earnings: number;
  max_delivery_distance_km: number;
  preferred_zones: string[];
  availability_schedule: {
    [day: string]: {
      start: string;
      end: string;
    };
  };
  is_independent: boolean;
}
```

### RestaurantAdvertisement

```typescript
interface RestaurantAdvertisement {
  id: number;
  restaurant: number;
  restaurant_name: string;
  ad_type: 'banner' | 'featured' | 'promotion' | 'sponsored';
  title: string;
  description: string;
  image: string;
  target_cities: string[];
  target_age_min: number | null;
  target_age_max: number | null;
  start_date: string;
  end_date: string;
  status: 'draft' | 'active' | 'paused' | 'completed';
  budget: number;
  cost_per_click: number;
  impressions: number;
  clicks: number;
  conversions: number;
  click_through_rate: number;
  conversion_rate: number;
  total_cost: number;
  created_at: string;
  updated_at: string;
}
```

### SocialMediaShare

```typescript
interface SocialMediaShare {
  id: number;
  restaurant: number;
  restaurant_name: string;
  platform: 'whatsapp' | 'facebook' | 'instagram' | 'twitter' | 'in_app';
  share_type: 'restaurant' | 'menu_item' | 'promotion';
  menu_item: number | null;
  promotion: number | null;
  title: string;
  message: string;
  image_url: string;
  share_url: string;
  views: number;
  clicks: number;
  shares_count: number;
  shared_by: number | null;
  shared_by_username: string | null;
  shared_at: string;
}
```

### PushNotificationCampaign

```typescript
interface PushNotificationCampaign {
  id: number;
  restaurant: number;
  restaurant_name: string;
  title: string;
  message: string;
  target_all_customers: boolean;
  target_favorites: boolean;
  target_previous_orders: boolean;
  status: 'draft' | 'scheduled' | 'sent' | 'cancelled';
  scheduled_at: string | null;
  sent_at: string | null;
  action_type: 'menu' | 'promotion' | 'order';
  action_data: {
    [key: string]: any;
  };
  recipients_count: number;
  delivered_count: number;
  opened_count: number;
  clicked_count: number;
  open_rate: number;
  click_rate: number;
  created_at: string;
  updated_at: string;
}
```

---

## Workflows

### Workflow : Restaurant Crée un Livreur

```
1. Restaurant se connecte
   ↓
2. Accède à "Gérer les livreurs"
   ↓
3. Clique sur "Ajouter un livreur"
   ↓
4. Remplit le formulaire (nom, email, téléphone, véhicule)
   ↓
5. Soumission → API crée le compte
   ↓
6. Livreur reçoit email/SMS avec identifiants
   ↓
7. Livreur se connecte et complète son profil
   ↓
8. Restaurant peut suivre les performances du livreur
```

### Workflow : Partage sur WhatsApp

```
1. Utilisateur voit un restaurant/plat intéressant
   ↓
2. Clique sur bouton "Partager"
   ↓
3. Sélectionne "WhatsApp"
   ↓
4. API génère le lien et le message formaté
   ↓
5. App ouvre WhatsApp avec message pré-rempli
   ↓
6. Utilisateur choisit contacts et envoie
   ↓
7. Métriques enregistrées (partage créé)
   ↓
8. Quand destinataire clique → +1 clic enregistré
```

### Workflow : Campagne Push Notification

```
1. Restaurant crée une campagne
   ↓
2. Définit le ciblage (favoris, clients précédents)
   ↓
3. Rédige titre et message
   ↓
4. Planifie ou envoie immédiatement
   ↓
5. Backend identifie les destinataires
   ↓
6. Notifications envoyées via Firebase
   ↓
7. Utilisateurs reçoivent la notification
   ↓
8. Métriques trackées (délivrées, ouvertes, cliquées)
```

---

## Sécurité et Permissions

### Règles de Permissions

**Gestion des Livreurs** :
- ✅ Restaurant peut créer/voir/modifier ses propres livreurs
- ✅ Livreur peut voir/modifier son propre profil
- ✅ Admin peut voir/modifier tous les livreurs
- ❌ Clients ne peuvent pas accéder aux profils livreurs (sauf via commandes)

**Marketing** :
- ✅ Restaurant peut créer ses propres campagnes
- ✅ Restaurant peut voir ses propres statistiques
- ✅ Tous les utilisateurs peuvent partager
- ✅ Admin peut voir toutes les campagnes

### Validation des Données

**Création de Livreur** :
- Email unique et valide
- Téléphone unique et valide au format international
- Mot de passe minimum 8 caractères
- Plaque d'immatriculation requise

**Campagnes** :
- Titre max 100 caractères
- Message max 200 caractères
- Date de planification future uniquement
- Budget > 0 pour les publicités

---

## Métriques et Analytics

### Métriques de Livreurs

- Nombre total de livraisons
- Note moyenne et nombre d'évaluations
- Total des pourboires
- Total des revenus
- Performance sur 30 derniers jours

### Métriques de Marketing

**Publicités** :
- Impressions
- Clics (CTR = clics / impressions)
- Conversions (CR = conversions / clics)
- Coût total

**Partages** :
- Nombre de partages par plateforme
- Vues et clics sur liens partagés
- Taux de conversion

**Push Notifications** :
- Destinataires ciblés
- Délivrées
- Ouvertes (Open Rate)
- Cliquées (Click Rate)

---

## Intégration Mobile

### Redux Slices Recommandées

```typescript
// driversSlice.ts
import { createApi } from '@reduxjs/toolkit/query/react';

export const driversApi = createApi({
  reducerPath: 'driversApi',
  baseQuery: fetchBaseQuery({ baseUrl: API_URL }),
  tagTypes: ['Driver'],
  endpoints: (builder) => ({
    getDrivers: builder.query({
      query: (params) => `/auth/drivers/?${new URLSearchParams(params)}`,
      providesTags: ['Driver'],
    }),
    createDriver: builder.mutation({
      query: (driverData) => ({
        url: '/auth/drivers/',
        method: 'POST',
        body: driverData,
      }),
      invalidatesTags: ['Driver'],
    }),
    updateDriverAvailability: builder.mutation({
      query: ({ driverId, is_available }) => ({
        url: `/auth/drivers/${driverId}/update_availability/`,
        method: 'PATCH',
        body: { is_available },
      }),
      invalidatesTags: ['Driver'],
    }),
    // ... autres endpoints
  }),
});

// marketingSlice.ts
export const marketingApi = createApi({
  reducerPath: 'marketingApi',
  baseQuery: fetchBaseQuery({ baseUrl: API_URL }),
  tagTypes: ['Share', 'Campaign'],
  endpoints: (builder) => ({
    quickShare: builder.mutation({
      query: (shareData) => ({
        url: '/marketing/shares/quick_share/',
        method: 'POST',
        body: shareData,
      }),
    }),
    getShareAnalytics: builder.query({
      query: (params) => `/marketing/shares/analytics/?${new URLSearchParams(params)}`,
    }),
    // ... autres endpoints
  }),
});
```

---

## Conclusion

Ces deux nouvelles fonctionnalités transforment la plateforme Multi-Restaurants en une solution complète :

✅ **Gestion des Livreurs** : Les restaurants ont le contrôle total sur leur flotte de livraison
✅ **Marketing** : Les restaurants peuvent promouvoir activement leurs services
✅ **Analytics** : Suivi détaillé des performances et de l'engagement
✅ **Intégration facile** : API RESTful claire et documentée

Pour toute question ou support, consultez la documentation API complète via `/api/v1/swagger/`.
