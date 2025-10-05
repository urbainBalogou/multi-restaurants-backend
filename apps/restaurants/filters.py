import django_filters
from .models import Restaurant, MenuItem


class RestaurantFilter(django_filters.FilterSet):
    min_rating = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    max_delivery_fee = django_filters.NumberFilter(field_name='delivery_fee', lookup_expr='lte')
    max_delivery_time = django_filters.NumberFilter(field_name='estimated_delivery_time', lookup_expr='lte')
    category = django_filters.CharFilter(method='filter_by_category')

    class Meta:
        model = Restaurant
        fields = ['is_accepting_orders', 'min_rating', 'max_delivery_fee', 'max_delivery_time']

    def filter_by_category(self, queryset, name, value):
        """Filtre les restaurants qui ont des plats dans une catégorie donnée"""
        return queryset.filter(menu_items__category__name__icontains=value).distinct()


class MenuItemFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    vegetarian = django_filters.BooleanFilter(method='filter_vegetarian')

    class Meta:
        model = MenuItem
        fields = ['restaurant', 'category', 'is_available', 'min_price', 'max_price']

    def filter_vegetarian(self, queryset, name, value):
        if value:
            return queryset.exclude(allergens__contains='meat')
        return queryset