# UI/UX Design Guidelines - Multi-Restaurants Mobile App

## Table des matières
1. [Système de couleurs](#système-de-couleurs)
2. [Typographie](#typographie)
3. [Espacement et grilles](#espacement-et-grilles)
4. [Composants UI](#composants-ui)
5. [Icônes et illustrations](#icônes-et-illustrations)
6. [Animations et transitions](#animations-et-transitions)
7. [Accessibilité](#accessibilité)
8. [Mode sombre](#mode-sombre)
9. [Design patterns](#design-patterns)
10. [Wireframes et flux utilisateur](#wireframes-et-flux-utilisateur)

---

## Système de couleurs

### Palette principale

```javascript
const colors = {
  // Couleurs primaires
  primary: {
    main: '#FF6B35',      // Orange vif - Action principale
    light: '#FF8C61',     // Orange clair - Hover states
    dark: '#E64D1F',      // Orange foncé - Active states
    contrast: '#FFFFFF',  // Texte sur fond primaire
  },

  // Couleurs secondaires
  secondary: {
    main: '#2D3142',      // Bleu foncé - Headers, navigation
    light: '#4F5D75',     // Bleu moyen
    dark: '#1A1E2E',      // Bleu très foncé
    contrast: '#FFFFFF',
  },

  // Couleurs d'accent
  accent: {
    success: '#10B981',   // Vert - Succès, disponible
    warning: '#F59E0B',   // Jaune - Attention, en attente
    error: '#EF4444',     // Rouge - Erreur, annulé
    info: '#3B82F6',      // Bleu - Information
  },

  // Couleurs neutres
  neutral: {
    50: '#F9FAFB',        // Fond très clair
    100: '#F3F4F6',       // Fond clair
    200: '#E5E7EB',       // Bordures légères
    300: '#D1D5DB',       // Bordures
    400: '#9CA3AF',       // Texte désactivé
    500: '#6B7280',       // Texte secondaire
    600: '#4B5563',       // Texte normal
    700: '#374151',       // Texte important
    800: '#1F2937',       // Texte très important
    900: '#111827',       // Texte principal
  },

  // Couleurs spécifiques
  rating: '#FFC107',      // Étoiles de notation
  premium: '#9333EA',     // Fonctionnalités premium
  delivery: '#06B6D4',    // Icônes de livraison

  // Arrière-plans
  background: {
    default: '#FFFFFF',
    paper: '#F9FAFB',
    elevated: '#FFFFFF',
  },

  // Texte
  text: {
    primary: '#111827',
    secondary: '#6B7280',
    disabled: '#9CA3AF',
    hint: '#D1D5DB',
  },
};
```

### Utilisation des couleurs

**Boutons d'action principale** : `primary.main`
- Ajouter au panier
- Commander maintenant
- Confirmer la commande
- Accepter une livraison

**Boutons secondaires** : `secondary.main` ou outline avec `primary.main`
- Annuler
- Retour
- Voir plus

**États de commande** :
- En attente : `accent.warning`
- En préparation : `accent.info`
- Prête : `accent.success`
- En livraison : `delivery`
- Livrée : `accent.success`
- Annulée : `accent.error`

**Indicateurs visuels** :
- Restaurant ouvert : `accent.success`
- Restaurant fermé : `accent.error`
- Livreur disponible : `accent.success`
- Promotion active : `accent.warning`

---

## Typographie

### Famille de polices

```javascript
const fonts = {
  primary: 'Inter',           // Police principale pour le texte
  headings: 'Poppins',        // Police pour les titres
  numbers: 'SF Mono',         // Police pour les prix et numéros
};
```

**Installation** :
```bash
# Pour React Native
npx expo install expo-font @expo-google-fonts/inter @expo-google-fonts/poppins
```

### Échelle typographique

```javascript
const typography = {
  // Titres
  h1: {
    fontFamily: 'Poppins-Bold',
    fontSize: 32,
    lineHeight: 40,
    letterSpacing: -0.5,
    fontWeight: '700',
  },

  h2: {
    fontFamily: 'Poppins-Bold',
    fontSize: 28,
    lineHeight: 36,
    letterSpacing: -0.5,
    fontWeight: '700',
  },

  h3: {
    fontFamily: 'Poppins-SemiBold',
    fontSize: 24,
    lineHeight: 32,
    letterSpacing: -0.25,
    fontWeight: '600',
  },

  h4: {
    fontFamily: 'Poppins-SemiBold',
    fontSize: 20,
    lineHeight: 28,
    letterSpacing: -0.25,
    fontWeight: '600',
  },

  h5: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    lineHeight: 24,
    letterSpacing: 0,
    fontWeight: '500',
  },

  h6: {
    fontFamily: 'Poppins-Medium',
    fontSize: 16,
    lineHeight: 22,
    letterSpacing: 0,
    fontWeight: '500',
  },

  // Corps de texte
  body1: {
    fontFamily: 'Inter-Regular',
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0.15,
    fontWeight: '400',
  },

  body2: {
    fontFamily: 'Inter-Regular',
    fontSize: 14,
    lineHeight: 20,
    letterSpacing: 0.15,
    fontWeight: '400',
  },

  // Texte spécialisé
  subtitle1: {
    fontFamily: 'Inter-Medium',
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0.15,
    fontWeight: '500',
  },

  subtitle2: {
    fontFamily: 'Inter-Medium',
    fontSize: 14,
    lineHeight: 20,
    letterSpacing: 0.1,
    fontWeight: '500',
  },

  caption: {
    fontFamily: 'Inter-Regular',
    fontSize: 12,
    lineHeight: 16,
    letterSpacing: 0.4,
    fontWeight: '400',
  },

  overline: {
    fontFamily: 'Inter-Medium',
    fontSize: 10,
    lineHeight: 14,
    letterSpacing: 1.5,
    fontWeight: '500',
    textTransform: 'uppercase',
  },

  button: {
    fontFamily: 'Inter-SemiBold',
    fontSize: 16,
    lineHeight: 24,
    letterSpacing: 0.5,
    fontWeight: '600',
    textTransform: 'uppercase',
  },

  // Prix
  price: {
    fontFamily: 'SF Mono',
    fontSize: 18,
    lineHeight: 24,
    letterSpacing: 0,
    fontWeight: '600',
  },
};
```

### Hiérarchie de l'information

**Écrans de liste** :
- Titre de l'écran : `h3`
- Nom du restaurant : `h6`
- Description : `body2`
- Prix : `price`
- Labels/badges : `caption` ou `overline`

**Écran de détail** :
- Titre : `h2`
- Section headers : `h5`
- Contenu principal : `body1`
- Informations secondaires : `body2`
- Métadonnées : `caption`

---

## Espacement et grilles

### Système d'espacement

Basé sur une unité de base de **8px** :

```javascript
const spacing = {
  xxs: 4,    // 0.5 unités
  xs: 8,     // 1 unité
  sm: 12,    // 1.5 unités
  md: 16,    // 2 unités
  lg: 24,    // 3 unités
  xl: 32,    // 4 unités
  xxl: 48,   // 6 unités
  xxxl: 64,  // 8 unités
};
```

### Marges et paddings

**Écrans** :
- Padding horizontal : `spacing.md` (16px)
- Padding vertical : `spacing.lg` (24px)
- Espacement entre sections : `spacing.xl` (32px)

**Cartes** :
- Padding interne : `spacing.md` (16px)
- Espacement entre cartes : `spacing.md` (16px)
- Border radius : 12px

**Listes** :
- Espacement entre items : `spacing.sm` (12px)
- Padding de l'item : `spacing.md` (16px)

**Formulaires** :
- Espacement entre champs : `spacing.md` (16px)
- Padding du champ : `spacing.sm` (12px) vertical, `spacing.md` (16px) horizontal
- Espacement label-champ : `spacing.xs` (8px)

### Grille responsive

```javascript
const grid = {
  columns: 12,
  gutter: spacing.md,
  margin: spacing.md,

  breakpoints: {
    xs: 0,      // Téléphones en portrait
    sm: 600,    // Téléphones en paysage / Petites tablettes
    md: 960,    // Tablettes
    lg: 1280,   // Ordinateurs portables
    xl: 1920,   // Grands écrans
  },
};
```

---

## Composants UI

### Boutons

#### Bouton primaire
```javascript
const primaryButton = {
  backgroundColor: colors.primary.main,
  borderRadius: 8,
  paddingVertical: spacing.sm,
  paddingHorizontal: spacing.lg,
  height: 48,

  // États
  hover: {
    backgroundColor: colors.primary.light,
  },
  pressed: {
    backgroundColor: colors.primary.dark,
  },
  disabled: {
    backgroundColor: colors.neutral[300],
    opacity: 0.6,
  },

  // Texte
  text: {
    ...typography.button,
    color: colors.primary.contrast,
  },
};
```

#### Bouton secondaire (outline)
```javascript
const secondaryButton = {
  backgroundColor: 'transparent',
  borderWidth: 2,
  borderColor: colors.primary.main,
  borderRadius: 8,
  paddingVertical: spacing.sm - 2, // Compenser la bordure
  paddingHorizontal: spacing.lg,
  height: 48,

  text: {
    ...typography.button,
    color: colors.primary.main,
  },
};
```

#### Bouton icône
```javascript
const iconButton = {
  width: 44,
  height: 44,
  borderRadius: 22,
  justifyContent: 'center',
  alignItems: 'center',
  backgroundColor: colors.neutral[100],

  // Taille de l'icône
  iconSize: 24,
};
```

#### Bouton flottant (FAB)
```javascript
const fab = {
  position: 'absolute',
  bottom: spacing.lg,
  right: spacing.md,
  width: 56,
  height: 56,
  borderRadius: 28,
  backgroundColor: colors.primary.main,
  elevation: 6,
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 3 },
  shadowOpacity: 0.3,
  shadowRadius: 4.65,
};
```

### Cartes (Cards)

#### Carte de restaurant
```javascript
const restaurantCard = {
  backgroundColor: colors.background.paper,
  borderRadius: 12,
  overflow: 'hidden',
  marginBottom: spacing.md,

  // Shadow
  elevation: 2,
  shadowColor: '#000',
  shadowOffset: { width: 0, height: 2 },
  shadowOpacity: 0.1,
  shadowRadius: 3.84,

  image: {
    width: '100%',
    height: 180,
    resizeMode: 'cover',
  },

  content: {
    padding: spacing.md,
  },

  badge: {
    position: 'absolute',
    top: spacing.sm,
    left: spacing.sm,
    backgroundColor: colors.primary.main,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xxs,
    borderRadius: 4,
  },
};
```

#### Carte de plat (menu item)
```javascript
const menuItemCard = {
  flexDirection: 'row',
  backgroundColor: colors.background.paper,
  borderRadius: 12,
  padding: spacing.md,
  marginBottom: spacing.sm,

  image: {
    width: 80,
    height: 80,
    borderRadius: 8,
    marginRight: spacing.md,
  },

  content: {
    flex: 1,
    justifyContent: 'space-between',
  },
};
```

### Inputs (Champs de saisie)

```javascript
const textInput = {
  height: 48,
  backgroundColor: colors.neutral[50],
  borderWidth: 1,
  borderColor: colors.neutral[300],
  borderRadius: 8,
  paddingHorizontal: spacing.md,
  fontSize: 16,
  color: colors.text.primary,

  // États
  focused: {
    borderColor: colors.primary.main,
    borderWidth: 2,
    backgroundColor: colors.background.default,
  },

  error: {
    borderColor: colors.accent.error,
  },

  disabled: {
    backgroundColor: colors.neutral[100],
    color: colors.text.disabled,
  },

  // Label
  label: {
    ...typography.subtitle2,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },

  // Message d'erreur
  errorMessage: {
    ...typography.caption,
    color: colors.accent.error,
    marginTop: spacing.xxs,
  },
};
```

### Badges et labels

```javascript
const badge = {
  // Badge de statut
  status: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xxs,
    borderRadius: 12,

    text: {
      ...typography.caption,
      fontWeight: '600',
    },

    // Variantes
    success: {
      backgroundColor: '#D1FAE5',
      color: '#065F46',
    },
    warning: {
      backgroundColor: '#FEF3C7',
      color: '#92400E',
    },
    error: {
      backgroundColor: '#FEE2E2',
      color: '#991B1B',
    },
    info: {
      backgroundColor: '#DBEAFE',
      color: '#1E40AF',
    },
  },

  // Badge de notification
  notification: {
    minWidth: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: colors.accent.error,
    justifyContent: 'center',
    alignItems: 'center',

    text: {
      ...typography.caption,
      color: '#FFFFFF',
      fontSize: 10,
      fontWeight: '700',
    },
  },
};
```

### Bottom Navigation Bar

```javascript
const bottomNavigation = {
  height: 60,
  backgroundColor: colors.background.default,
  borderTopWidth: 1,
  borderTopColor: colors.neutral[200],
  flexDirection: 'row',

  // Shadow sur iOS
  shadowColor: '#000',
  shadowOffset: { width: 0, height: -2 },
  shadowOpacity: 0.1,
  shadowRadius: 3,

  // Elevation sur Android
  elevation: 8,

  item: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',

    icon: {
      size: 24,
      marginBottom: 4,
    },

    label: {
      ...typography.caption,
      fontSize: 11,
    },

    // États
    active: {
      iconColor: colors.primary.main,
      labelColor: colors.primary.main,
    },
    inactive: {
      iconColor: colors.text.secondary,
      labelColor: colors.text.secondary,
    },
  },
};
```

### Modal / Bottom Sheet

```javascript
const modal = {
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'flex-end',
  },

  container: {
    backgroundColor: colors.background.default,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingTop: spacing.md,
    paddingHorizontal: spacing.md,
    paddingBottom: spacing.xl,
    maxHeight: '90%',
  },

  handle: {
    width: 40,
    height: 4,
    backgroundColor: colors.neutral[300],
    borderRadius: 2,
    alignSelf: 'center',
    marginBottom: spacing.md,
  },
};
```

### Loading States

```javascript
const skeleton = {
  backgroundColor: colors.neutral[200],
  borderRadius: 4,

  // Animation shimmer
  shimmer: {
    backgroundColor: colors.neutral[100],
    // Utiliser react-native-linear-gradient pour l'effet shimmer
  },
};

const spinner = {
  size: 'large',
  color: colors.primary.main,
};
```

---

## Icônes et illustrations

### Bibliothèque d'icônes

**Recommandé** : `@expo/vector-icons` avec Ionicons

```javascript
import { Ionicons } from '@expo/vector-icons';

const iconLibrary = {
  // Navigation
  home: 'home-outline',
  search: 'search-outline',
  orders: 'receipt-outline',
  profile: 'person-outline',

  // Actions
  add: 'add-circle-outline',
  remove: 'remove-circle-outline',
  close: 'close-outline',
  back: 'arrow-back-outline',
  forward: 'arrow-forward-outline',

  // Restaurant
  restaurant: 'restaurant-outline',
  star: 'star',
  starOutline: 'star-outline',
  location: 'location-outline',
  time: 'time-outline',

  // Livraison
  delivery: 'bicycle-outline',
  car: 'car-outline',
  map: 'map-outline',
  navigation: 'navigate-outline',

  // Commande
  cart: 'cart-outline',
  bag: 'bag-handle-outline',
  card: 'card-outline',
  cash: 'cash-outline',

  // Communication
  chat: 'chatbubble-outline',
  call: 'call-outline',
  notifications: 'notifications-outline',

  // Profil
  settings: 'settings-outline',
  logout: 'log-out-outline',
  edit: 'create-outline',
  camera: 'camera-outline',

  // Autre
  filter: 'filter-outline',
  heart: 'heart-outline',
  heartFilled: 'heart',
  share: 'share-social-outline',
  info: 'information-circle-outline',
  warning: 'warning-outline',
  checkmark: 'checkmark-circle-outline',
};
```

### Tailles d'icônes

```javascript
const iconSizes = {
  xs: 16,
  sm: 20,
  md: 24,
  lg: 32,
  xl: 48,
};
```

### Illustrations

**Écrans vides** : Utiliser illustrations minimalistes pour :
- Panier vide
- Aucune commande
- Aucun restaurant trouvé
- Erreur de connexion
- Localisation désactivée

**Source recommandée** :
- undraw.co (illustrations vectorielles gratuites)
- Lottie animations (lottiefiles.com)

---

## Animations et transitions

### Durées

```javascript
const duration = {
  fastest: 150,  // Micro-interactions
  fast: 250,     // Transitions rapides
  normal: 350,   // Transitions standard
  slow: 500,     // Transitions élaborées
};
```

### Courbes d'animation (Easing)

```javascript
import { Easing } from 'react-native';

const easing = {
  easeInOut: Easing.bezier(0.4, 0, 0.2, 1),
  easeOut: Easing.bezier(0, 0, 0.2, 1),
  easeIn: Easing.bezier(0.4, 0, 1, 1),
  sharp: Easing.bezier(0.4, 0, 0.6, 1),
};
```

### Animations courantes

#### Fade In/Out
```javascript
import { Animated } from 'react-native';

const fadeIn = (animatedValue) => {
  Animated.timing(animatedValue, {
    toValue: 1,
    duration: duration.fast,
    easing: easing.easeOut,
    useNativeDriver: true,
  }).start();
};
```

#### Slide Up (Bottom Sheet)
```javascript
const slideUp = (animatedValue) => {
  Animated.spring(animatedValue, {
    toValue: 0,
    friction: 8,
    tension: 40,
    useNativeDriver: true,
  }).start();
};
```

#### Scale (Bouton pressé)
```javascript
const scaleDown = (animatedValue) => {
  Animated.sequence([
    Animated.timing(animatedValue, {
      toValue: 0.95,
      duration: duration.fastest,
      useNativeDriver: true,
    }),
    Animated.timing(animatedValue, {
      toValue: 1,
      duration: duration.fastest,
      useNativeDriver: true,
    }),
  ]).start();
};
```

#### Shimmer (Loading)
```javascript
const shimmer = (animatedValue) => {
  Animated.loop(
    Animated.sequence([
      Animated.timing(animatedValue, {
        toValue: 1,
        duration: 1000,
        easing: Easing.linear,
        useNativeDriver: true,
      }),
      Animated.timing(animatedValue, {
        toValue: 0,
        duration: 1000,
        easing: Easing.linear,
        useNativeDriver: true,
      }),
    ])
  ).start();
};
```

### Transitions d'écran

**React Navigation** :
```javascript
const screenOptions = {
  headerShown: false,
  cardStyleInterpolator: ({ current, layouts }) => {
    return {
      cardStyle: {
        transform: [
          {
            translateX: current.progress.interpolate({
              inputRange: [0, 1],
              outputRange: [layouts.screen.width, 0],
            }),
          },
        ],
      },
    };
  },
  transitionSpec: {
    open: {
      animation: 'timing',
      config: {
        duration: duration.normal,
        easing: easing.easeOut,
      },
    },
    close: {
      animation: 'timing',
      config: {
        duration: duration.normal,
        easing: easing.easeIn,
      },
    },
  },
};
```

### Micro-interactions

**Ajout au panier** :
1. Bounce de l'icône panier
2. Affichage d'un badge avec le nouveau nombre
3. Toast de confirmation

**Like/Favori** :
1. Scale up de l'icône
2. Changement de couleur (outline → filled)
3. Haptic feedback

**Pull to refresh** :
1. Indicateur de chargement
2. Animation de rotation
3. Feedback de succès

---

## Accessibilité

### Taille minimale des zones tactiles

```javascript
const touchTarget = {
  minWidth: 44,
  minHeight: 44,
};
```

### Labels pour lecteurs d'écran

```jsx
<TouchableOpacity
  accessible={true}
  accessibilityLabel="Ajouter au panier"
  accessibilityHint="Ajoute cet article à votre panier"
  accessibilityRole="button"
>
  <Text>Ajouter</Text>
</TouchableOpacity>
```

### Contraste des couleurs

**Ratio minimum** :
- Texte normal : 4.5:1
- Texte large (18pt+) : 3:1
- Éléments d'interface : 3:1

**Vérification** : Utiliser WebAIM Contrast Checker

### Support du mode haute lisibilité

```javascript
import { AccessibilityInfo } from 'react-native';

const [isBoldTextEnabled, setIsBoldTextEnabled] = useState(false);

useEffect(() => {
  AccessibilityInfo.isBoldTextEnabled().then(setIsBoldTextEnabled);
}, []);

// Ajuster la typographie si nécessaire
const textStyle = {
  ...typography.body1,
  fontWeight: isBoldTextEnabled ? '600' : '400',
};
```

### Navigation au clavier (pour tablettes)

- Support de Tab pour la navigation
- Indicateurs visuels de focus
- Raccourcis clavier pour actions principales

---

## Mode sombre

### Palette de couleurs sombres

```javascript
const darkColors = {
  // Couleurs primaires (légèrement désaturées)
  primary: {
    main: '#FF7A50',
    light: '#FF9876',
    dark: '#E65F39',
    contrast: '#FFFFFF',
  },

  // Couleurs secondaires
  secondary: {
    main: '#E5E7EB',
    light: '#F3F4F6',
    dark: '#D1D5DB',
    contrast: '#111827',
  },

  // Couleurs d'accent (ajustées pour le contraste)
  accent: {
    success: '#34D399',
    warning: '#FBBF24',
    error: '#F87171',
    info: '#60A5FA',
  },

  // Couleurs neutres inversées
  neutral: {
    50: '#111827',
    100: '#1F2937',
    200: '#374151',
    300: '#4B5563',
    400: '#6B7280',
    500: '#9CA3AF',
    600: '#D1D5DB',
    700: '#E5E7EB',
    800: '#F3F4F6',
    900: '#F9FAFB',
  },

  // Arrière-plans
  background: {
    default: '#111827',
    paper: '#1F2937',
    elevated: '#374151',
  },

  // Texte
  text: {
    primary: '#F9FAFB',
    secondary: '#D1D5DB',
    disabled: '#6B7280',
    hint: '#4B5563',
  },
};
```

### Implémentation

```javascript
import { useColorScheme } from 'react-native';

const MyComponent = () => {
  const scheme = useColorScheme();
  const isDarkMode = scheme === 'dark';

  const currentColors = isDarkMode ? darkColors : colors;

  return (
    <View style={{ backgroundColor: currentColors.background.default }}>
      <Text style={{ color: currentColors.text.primary }}>
        Contenu
      </Text>
    </View>
  );
};
```

### Considérations pour le mode sombre

- **Images** : Réduire légèrement l'opacité (0.85) pour éviter l'éblouissement
- **Ombres** : Utiliser des ombres plus subtiles
- **Bordures** : Augmenter légèrement le contraste
- **Icônes** : Utiliser des versions outline plutôt que filled

---

## Design Patterns

### Pattern de navigation

**Architecture de navigation** :
```
Bottom Tab Navigator (principal)
├── Home Stack
│   ├── Home Screen
│   ├── Restaurant Detail
│   ├── Menu Item Detail
│   └── Cart
├── Search Stack
│   ├── Search Screen
│   └── Results
├── Orders Stack
│   ├── Orders List
│   ├── Order Detail
│   └── Track Order
└── Profile Stack
    ├── Profile Screen
    ├── Edit Profile
    ├── Settings
    └── Favorites
```

### Pattern de liste

**Liste infinie avec pagination** :
```jsx
<FlatList
  data={items}
  renderItem={({ item }) => <RestaurantCard {...item} />}
  keyExtractor={(item) => item.id.toString()}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
  ListEmptyComponent={<EmptyState />}
  ListFooterComponent={loading ? <LoadingIndicator /> : null}
  refreshControl={
    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
  }
/>
```

### Pattern de recherche

**Recherche avec debounce** :
```jsx
const [searchQuery, setSearchQuery] = useState('');
const debouncedSearch = useDebounce(searchQuery, 500);

useEffect(() => {
  if (debouncedSearch) {
    performSearch(debouncedSearch);
  }
}, [debouncedSearch]);
```

### Pattern de formulaire

**Validation en temps réel** :
```jsx
const [formData, setFormData] = useState({});
const [errors, setErrors] = useState({});

const validateField = (name, value) => {
  // Logique de validation
  const error = validate(name, value);
  setErrors(prev => ({ ...prev, [name]: error }));
};

const handleChange = (name, value) => {
  setFormData(prev => ({ ...prev, [name]: value }));
  validateField(name, value);
};
```

### Pattern de confirmation

**Action destructive** :
```jsx
const handleDelete = () => {
  Alert.alert(
    'Confirmer la suppression',
    'Êtes-vous sûr de vouloir supprimer cet élément ?',
    [
      { text: 'Annuler', style: 'cancel' },
      {
        text: 'Supprimer',
        style: 'destructive',
        onPress: () => performDelete()
      },
    ]
  );
};
```

---

## Wireframes et flux utilisateur

### Flux d'inscription/connexion

```
1. Welcome Screen
   ├─> Connexion
   │   ├─> Email + Password
   │   ├─> Forgot Password
   │   └─> Success → Home
   └─> Inscription
       ├─> Sélection du rôle (Client/Restaurant/Livreur)
       ├─> Informations de base
       ├─> Vérification email/téléphone
       └─> Success → Home (ou profil incomplet)
```

### Flux de commande (Client)

```
1. Home → Recherche/Browse restaurants
2. Sélection restaurant → Restaurant Detail
3. Ajout d'articles → Cart
4. Review Cart → Add more / Proceed to Checkout
5. Checkout
   ├─> Adresse de livraison (sélection/ajout)
   ├─> Heure de livraison
   ├─> Instructions spéciales
   └─> Méthode de paiement
6. Confirmation de commande
7. Suivi en temps réel
8. Notification de livraison
9. Évaluation (restaurant + livreur)
```

### Flux de gestion de commande (Restaurant)

```
1. Dashboard → Nouvelles commandes (notification)
2. Détail de la commande
   ├─> Accepter → Temps de préparation estimé
   │   └─> Marquer comme "En préparation"
   │       └─> Marquer comme "Prête"
   └─> Refuser → Raison du refus
3. Historique des commandes
```

### Flux de livraison (Livreur)

```
1. Dashboard → Commandes disponibles
2. Sélection de commande → Détails
3. Accepter → Navigation vers restaurant
4. Arrivée au restaurant → Marquer "Récupérée"
5. Navigation vers client
6. Livraison → Marquer "Livrée"
   ├─> Code de confirmation
   └─> Photo de livraison (optionnel)
7. Fin de la livraison → Disponible pour nouvelle commande
```

### Wireframe: Home Screen (Client)

```
┌─────────────────────────────┐
│ [Logo]    [Location ▼]  [🔔]│ Header
├─────────────────────────────┤
│                             │
│ [Search bar with icon]      │ Search
│                             │
├─────────────────────────────┤
│ Catégories                  │
│ [🍕] [🍔] [🍜] [🍰] [→]      │ Horizontal scroll
├─────────────────────────────┤
│ Restaurants populaires      │
│ ┌─────────────────────────┐ │
│ │ [Image]                 │ │
│ │ Restaurant Name         │ │
│ │ ⭐ 4.5 | 25 min | 2.5km │ │
│ │ Cuisine type            │ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ [Image]                 │ │
│ │ ...                     │ │
│ └─────────────────────────┘ │
├─────────────────────────────┤
│ [🏠] [🔍] [📋] [👤]         │ Bottom Nav
└─────────────────────────────┘
```

### Wireframe: Restaurant Detail

```
┌─────────────────────────────┐
│ [←] Restaurant Name     [♡] │ Header
├─────────────────────────────┤
│                             │
│ [Large Image]               │
│                             │
├─────────────────────────────┤
│ ⭐ 4.5 (234 avis)           │
│ 🚴 25-35 min | 2.99€        │
│ 📍 Address                  │
│ ℹ️ Info | 💬 Avis          │
├─────────────────────────────┤
│ Menu                        │
│                             │
│ [Entrées ▼]                 │
│ ┌─────────────────────────┐ │
│ │ [Img] Item Name    4.99€│ │
│ │       Description   [+] │ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ ...                     │ │
│ └─────────────────────────┘ │
│                             │
│ [Plats principaux ▼]        │
│ ...                         │
├─────────────────────────────┤
│ [Panier (3)] 24.97€     [→]│ Sticky bottom
└─────────────────────────────┘
```

### Wireframe: Suivi de commande

```
┌─────────────────────────────┐
│ [←] Commande #12345         │
├─────────────────────────────┤
│                             │
│ [Map with route & markers]  │
│                             │
├─────────────────────────────┤
│ ● Commande confirmée   ✓    │
│ ● En préparation       ✓    │
│ ● Prête pour livraison ✓    │
│ ● En livraison         ●    │
│ ○ Livrée                    │
├─────────────────────────────┤
│ Estimé: 15 minutes          │
├─────────────────────────────┤
│ Livreur: Jean Dupont        │
│ ⭐ 4.8 (156 livraisons)     │
│ [📞 Appeler] [💬 Message]   │
├─────────────────────────────┤
│ Détails de la commande      │
│ 2x Burger Royal        15€  │
│ 1x Frites              3€   │
│ Livraison              2.99€│
│ ─────────────────────────   │
│ Total                  20.99€│
└─────────────────────────────┘
```

---

## Checklist UI/UX

### Avant le développement
- [ ] Design system documenté et partagé
- [ ] Palette de couleurs définie (clair + sombre)
- [ ] Typographie définie avec échelle cohérente
- [ ] Grille et système d'espacement établis
- [ ] Composants UI de base créés
- [ ] Bibliothèque d'icônes choisie
- [ ] Wireframes validés pour tous les écrans principaux
- [ ] Flux utilisateur documentés

### Pendant le développement
- [ ] Utilisation cohérente des couleurs du design system
- [ ] Respect de la hiérarchie typographique
- [ ] Espacement cohérent entre les éléments
- [ ] Zones tactiles de taille appropriée (min 44x44)
- [ ] États visuels pour tous les éléments interactifs (normal, hover, pressed, disabled)
- [ ] Animations fluides et non intrusives
- [ ] Loading states pour toutes les opérations asynchrones
- [ ] Empty states pour toutes les listes/collections
- [ ] Error states avec messages explicites
- [ ] Feedback visuel pour toutes les actions utilisateur

### Accessibilité
- [ ] Labels appropriés pour lecteurs d'écran
- [ ] Contraste suffisant pour tout le texte
- [ ] Support du mode sombre
- [ ] Support du mode haute lisibilité
- [ ] Navigation au clavier fonctionnelle
- [ ] Taille de police ajustable
- [ ] Réduction des animations si demandée par le système

### Performance
- [ ] Images optimisées et lazy-loaded
- [ ] Listes virtualisées (FlatList)
- [ ] Animations utilisant native driver
- [ ] Memoization des composants coûteux
- [ ] Debounce pour les recherches
- [ ] Pagination pour les longues listes

### Tests UI/UX
- [ ] Test sur différentes tailles d'écran
- [ ] Test sur iOS et Android
- [ ] Test en mode portrait et paysage
- [ ] Test avec mode sombre activé
- [ ] Test avec VoiceOver/TalkBack
- [ ] Test avec connexion lente
- [ ] Test des cas limites (textes très longs, listes vides, etc.)
- [ ] Test du parcours utilisateur complet

---

## Ressources et outils

### Design
- **Figma** : Design d'interface et prototypage
- **Adobe Color** : Création de palettes de couleurs
- **Coolors** : Générateur de palettes
- **WebAIM Contrast Checker** : Vérification du contraste

### Développement
- **React Native Paper** : Bibliothèque de composants Material Design
- **React Native Elements** : Bibliothèque de composants cross-platform
- **Styled Components** : CSS-in-JS pour React Native
- **React Native Reanimated** : Animations performantes
- **Lottie** : Animations vectorielles

### Icônes et illustrations
- **Ionicons** : Bibliothèque d'icônes
- **React Native Vector Icons** : Collection d'icônes
- **unDraw** : Illustrations open source
- **Lottie Files** : Animations Lottie gratuites

### Typographie
- **Google Fonts** : Polices open source
- **Expo Google Fonts** : Intégration facile dans Expo

### Inspiration
- **Dribbble** : Inspiration design
- **Behance** : Portfolios de designers
- **Mobbin** : Screenshots d'applications mobiles
- **UI8** : Templates et kits UI

---

## Conclusion

Ce guide UI/UX fournit une base solide pour créer une interface cohérente, accessible et agréable pour l'application Multi-Restaurants. Il est important de :

1. **Respecter le design system** : Utiliser systématiquement les couleurs, typographies et espacements définis
2. **Penser accessibilité** : Concevoir pour tous les utilisateurs, y compris ceux avec des besoins spécifiques
3. **Optimiser les performances** : Créer des animations fluides et des interfaces réactives
4. **Tester régulièrement** : Valider l'expérience sur différents appareils et conditions
5. **Itérer** : Améliorer continuellement basé sur les retours utilisateurs

N'hésitez pas à adapter ces guidelines selon les besoins spécifiques du projet tout en maintenant la cohérence globale.
