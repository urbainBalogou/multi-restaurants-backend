from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CouponViewSet, PromotionViewSet, CouponUsageViewSet

router = DefaultRouter()
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'promotions', PromotionViewSet, basename='promotion')
router.register(r'coupon-usage', CouponUsageViewSet, basename='coupon-usage')

urlpatterns = [
    path('', include(router.urls)),
]
