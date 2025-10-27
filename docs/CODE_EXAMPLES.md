# 💻 EXEMPLES DE CODE COMPLETS - Application Mobile

Ce document contient des **exemples de code prêts à utiliser** pour toutes les fonctionnalités principales de l'app.

---

## 📱 TABLE DES MATIÈRES

1. [Configuration Redux Store](#configuration-redux-store)
2. [Services API](#services-api)
3. [Authentification complète](#authentification-complète)
4. [Écrans principaux](#écrans-principaux)
5. [Composants réutilisables](#composants-réutilisables)
6. [Navigation](#navigation)
7. [Gestion du panier](#gestion-du-panier)
8. [Géolocalisation](#géolocalisation)
9. [Notifications Push](#notifications-push)
10. [Paiement Stripe](#paiement-stripe)

---

## 🔧 CONFIGURATION REDUX STORE

### store/index.js
```javascript
import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import cartReducer from './slices/cartSlice';
import restaurantReducer from './slices/restaurantSlice';
import orderReducer from './slices/orderSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    cart: cartReducer,
    restaurant: restaurantReducer,
    order: orderReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### store/slices/authSlice.js
```javascript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { authService } from '../../api/services/authService';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Actions asynchrones
export const loginUser = createAsyncThunk(
  'auth/login',
  async (credentials, { rejectWithValue }) => {
    try {
      const response = await authService.login(credentials);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const registerUser = createAsyncThunk(
  'auth/register',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await authService.register(userData);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);

export const loadUser = createAsyncThunk(
  'auth/loadUser',
  async (_, { rejectWithValue }) => {
    try {
      const user = await authService.getCurrentUser();
      return user;
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    token: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      authService.logout();
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload;
        state.token = action.payload.api_token;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    // Register
    builder
      .addCase(registerUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.data;
        state.token = action.payload.data.api_token;
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });

    // Load User
    builder
      .addCase(loadUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
      });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
```

### store/slices/cartSlice.js
```javascript
import { createSlice } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    restaurant: null,
    subtotal: 0,
    deliveryFee: 0,
    tax: 0,
    discount: 0,
    total: 0,
    coupon: null,
  },
  reducers: {
    addToCart: (state, action) => {
      const { item, restaurant } = action.payload;

      // Si nouveau restaurant, vider le panier
      if (state.restaurant && state.restaurant.id !== restaurant.id) {
        state.items = [];
      }

      state.restaurant = restaurant;

      // Chercher si l'item existe déjà (même options)
      const existingItemIndex = state.items.findIndex(
        (cartItem) =>
          cartItem.id === item.id &&
          JSON.stringify(cartItem.selectedOptions) === JSON.stringify(item.selectedOptions)
      );

      if (existingItemIndex >= 0) {
        state.items[existingItemIndex].quantity += item.quantity;
      } else {
        state.items.push(item);
      }

      cartSlice.caseReducers.calculateTotals(state);
      saveCartToStorage(state);
    },

    removeFromCart: (state, action) => {
      state.items = state.items.filter((item, index) => index !== action.payload);
      cartSlice.caseReducers.calculateTotals(state);
      saveCartToStorage(state);
    },

    updateQuantity: (state, action) => {
      const { index, quantity } = action.payload;
      if (quantity <= 0) {
        state.items = state.items.filter((_, i) => i !== index);
      } else {
        state.items[index].quantity = quantity;
      }
      cartSlice.caseReducers.calculateTotals(state);
      saveCartToStorage(state);
    },

    applyCoupon: (state, action) => {
      state.coupon = action.payload.coupon;
      state.discount = action.payload.discount_amount;
      cartSlice.caseReducers.calculateTotals(state);
    },

    removeCoupon: (state) => {
      state.coupon = null;
      state.discount = 0;
      cartSlice.caseReducers.calculateTotals(state);
    },

    setDeliveryFee: (state, action) => {
      state.deliveryFee = action.payload;
      cartSlice.caseReducers.calculateTotals(state);
    },

    clearCart: (state) => {
      state.items = [];
      state.restaurant = null;
      state.subtotal = 0;
      state.deliveryFee = 0;
      state.tax = 0;
      state.discount = 0;
      state.total = 0;
      state.coupon = null;
      AsyncStorage.removeItem('cart');
    },

    loadCart: (state, action) => {
      const cart = action.payload;
      state.items = cart.items || [];
      state.restaurant = cart.restaurant || null;
      state.deliveryFee = cart.deliveryFee || 0;
      state.coupon = cart.coupon || null;
      state.discount = cart.discount || 0;
      cartSlice.caseReducers.calculateTotals(state);
    },

    calculateTotals: (state) => {
      // Sous-total
      state.subtotal = state.items.reduce((total, item) => {
        const itemPrice = parseFloat(item.unit_price) * item.quantity;
        // Ajouter le prix des options
        if (item.selectedOptions) {
          const optionsPrice = Object.values(item.selectedOptions).reduce((sum, opt) => {
            if (Array.isArray(opt)) {
              return sum + opt.reduce((s, o) => s + (o.price || 0), 0);
            }
            return sum + (opt.price || 0);
          }, 0);
          return total + itemPrice + (optionsPrice * item.quantity);
        }
        return total + itemPrice;
      }, 0);

      // Taxe (10%)
      state.tax = state.subtotal * 0.1;

      // Total
      state.total = state.subtotal + state.deliveryFee + state.tax - state.discount;

      // Livraison gratuite si seuil atteint
      if (state.restaurant?.free_delivery_threshold) {
        const threshold = parseFloat(state.restaurant.free_delivery_threshold);
        if (state.subtotal >= threshold) {
          state.deliveryFee = 0;
        }
      }
    },
  },
});

// Sauvegarder dans AsyncStorage
const saveCartToStorage = async (state) => {
  try {
    await AsyncStorage.setItem('cart', JSON.stringify({
      items: state.items,
      restaurant: state.restaurant,
      deliveryFee: state.deliveryFee,
      coupon: state.coupon,
      discount: state.discount,
    }));
  } catch (error) {
    console.error('Error saving cart:', error);
  }
};

export const {
  addToCart,
  removeFromCart,
  updateQuantity,
  applyCoupon,
  removeCoupon,
  setDeliveryFee,
  clearCart,
  loadCart,
} = cartSlice.actions;

export default cartSlice.reducer;
```

---

## 🔐 AUTHENTIFICATION COMPLÈTE

### screens/auth/LoginScreen.js
```javascript
import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { loginUser, clearError } from '../../store/slices/authSlice';

const LoginScreen = ({ navigation }) => {
  const dispatch = useDispatch();
  const { loading, error } = useSelector((state) => state.auth);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }

    try {
      const result = await dispatch(loginUser({ email, password })).unwrap();
      // Navigation handled by App.js based on auth state
    } catch (error) {
      Alert.alert('Erreur', error.message || 'Connexion échouée');
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.formContainer}>
        <Text style={styles.title}>Connexion</Text>
        <Text style={styles.subtitle}>Bon retour parmi nous !</Text>

        <TextInput
          style={styles.input}
          placeholder="Email"
          placeholderTextColor="#999"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
          autoCorrect={false}
        />

        <TextInput
          style={styles.input}
          placeholder="Mot de passe"
          placeholderTextColor="#999"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          autoCapitalize="none"
        />

        <TouchableOpacity
          style={styles.forgotPassword}
          onPress={() => navigation.navigate('ForgotPassword')}
        >
          <Text style={styles.forgotPasswordText}>Mot de passe oublié ?</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Se connecter</Text>
          )}
        </TouchableOpacity>

        <View style={styles.registerContainer}>
          <Text style={styles.registerText}>Pas encore de compte ? </Text>
          <TouchableOpacity onPress={() => navigation.navigate('Register')}>
            <Text style={styles.registerLink}>S'inscrire</Text>
          </TouchableOpacity>
        </View>

        {error && (
          <View style={styles.errorContainer}>
            <Text style={styles.errorText}>{error.message || 'Une erreur est survenue'}</Text>
          </View>
        )}
      </View>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  formContainer: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 32,
  },
  input: {
    height: 56,
    backgroundColor: '#f5f5f5',
    borderRadius: 12,
    paddingHorizontal: 16,
    fontSize: 16,
    marginBottom: 16,
  },
  forgotPassword: {
    alignSelf: 'flex-end',
    marginBottom: 24,
  },
  forgotPasswordText: {
    color: '#FF6B6B',
    fontSize: 14,
  },
  button: {
    height: 56,
    backgroundColor: '#FF6B6B',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  buttonDisabled: {
    backgroundColor: '#FFB3B3',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
  },
  registerText: {
    color: '#666',
    fontSize: 14,
  },
  registerLink: {
    color: '#FF6B6B',
    fontSize: 14,
    fontWeight: '600',
  },
  errorContainer: {
    marginTop: 16,
    padding: 12,
    backgroundColor: '#FFE5E5',
    borderRadius: 8,
  },
  errorText: {
    color: '#FF0000',
    fontSize: 14,
    textAlign: 'center',
  },
});

export default LoginScreen;
```

---

## 🏠 ÉCRAN PRINCIPAL (HOME)

### screens/customer/HomeScreen.js
```javascript
import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { restaurantService } from '../../api/services/restaurantService';
import RestaurantCard from '../../components/restaurant/RestaurantCard';
import SearchBar from '../../components/common/SearchBar';
import CategoryScroll from '../../components/restaurant/CategoryScroll';
import useLocation from '../../hooks/useLocation';

const HomeScreen = ({ navigation }) => {
  const { user } = useSelector((state) => state.auth);
  const { location, requestLocation } = useLocation();

  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadRestaurants();
  }, [location]);

  const loadRestaurants = async () => {
    try {
      setLoading(true);

      let data;
      if (location) {
        // Restaurants à proximité
        data = await restaurantService.getNearbyRestaurants(
          location.latitude,
          location.longitude,
          10
        );
      } else {
        // Tous les restaurants
        data = await restaurantService.getRestaurants();
      }

      setRestaurants(data.results || data);
    } catch (error) {
      console.error('Error loading restaurants:', error);
      Alert.alert('Erreur', 'Impossible de charger les restaurants');
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadRestaurants();
    setRefreshing(false);
  };

  const filteredRestaurants = restaurants.filter((restaurant) =>
    restaurant.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF6B6B" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Bonjour {user?.first_name || user?.username} 👋</Text>
          <TouchableOpacity onPress={requestLocation} style={styles.locationButton}>
            <Text style={styles.location}>
              📍 {location ? 'Position actuelle' : 'Activer la localisation'}
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Rechercher un restaurant..."
        />
      </View>

      {/* Categories */}
      <CategoryScroll />

      {/* Restaurants List */}
      <FlatList
        data={filteredRestaurants}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <RestaurantCard
            restaurant={item}
            onPress={() => navigation.navigate('RestaurantDetail', { restaurant: item })}
          />
        )}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#FF6B6B']} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Aucun restaurant trouvé</Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    padding: 16,
    paddingTop: 50,
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#000',
    marginBottom: 4,
  },
  locationButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  location: {
    fontSize: 14,
    color: '#666',
  },
  searchContainer: {
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  listContent: {
    paddingHorizontal: 16,
    paddingBottom: 16,
  },
  emptyContainer: {
    padding: 32,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
  },
});

export default HomeScreen;
```

---

## 🍽️ COMPOSANT RESTAURANT CARD

### components/restaurant/RestaurantCard.js
```javascript
import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';
import FastImage from 'react-native-fast-image';

const RestaurantCard = ({ restaurant, onPress }) => {
  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.8}>
      <FastImage
        source={{
          uri: restaurant.image || 'https://via.placeholder.com/400x200',
          priority: FastImage.priority.normal,
        }}
        style={styles.image}
        resizeMode={FastImage.resizeMode.cover}
      />

      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.name} numberOfLines={1}>
            {restaurant.name}
          </Text>
          <View style={styles.ratingContainer}>
            <Text style={styles.rating}>⭐️ {restaurant.average_rating.toFixed(1)}</Text>
          </View>
        </View>

        <Text style={styles.description} numberOfLines={2}>
          {restaurant.description}
        </Text>

        <View style={styles.footer}>
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>🕐</Text>
            <Text style={styles.infoText}>{restaurant.estimated_delivery_time} min</Text>
          </View>

          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>🚚</Text>
            <Text style={styles.infoText}>
              {parseFloat(restaurant.delivery_fee) === 0
                ? 'Gratuit'
                : `${restaurant.delivery_fee}€`}
            </Text>
          </View>

          {restaurant.distance_km && (
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>📍</Text>
              <Text style={styles.infoText}>{restaurant.distance_km} km</Text>
            </View>
          )}
        </View>

        {!restaurant.is_accepting_orders && (
          <View style={styles.closedBadge}>
            <Text style={styles.closedText}>Fermé</Text>
          </View>
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
    overflow: 'hidden',
  },
  image: {
    width: '100%',
    height: 180,
  },
  content: {
    padding: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  name: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#000',
    flex: 1,
    marginRight: 8,
  },
  ratingContainer: {
    backgroundColor: '#FFF3E0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  rating: {
    fontSize: 14,
    fontWeight: '600',
    color: '#F57C00',
  },
  description: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  infoItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoLabel: {
    fontSize: 16,
    marginRight: 4,
  },
  infoText: {
    fontSize: 14,
    color: '#666',
  },
  closedBadge: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: '#FF6B6B',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  closedText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
});

export default RestaurantCard;
```

---

Je continue avec les autres fichiers essentiels...
