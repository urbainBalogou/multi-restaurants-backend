from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.restaurants.models import Restaurant
from .models import Coupon, Promotion

User = get_user_model()


class CouponModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.coupon = Coupon.objects.create(
            code='TEST20',
            discount_type='percentage',
            discount_value=20,
            min_order_amount=10,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=30)
        )

    def test_coupon_creation(self):
        self.assertEqual(self.coupon.code, 'TEST20')
        self.assertEqual(self.coupon.discount_value, 20)

    def test_coupon_is_valid(self):
        is_valid, message = self.coupon.is_valid()
        self.assertTrue(is_valid)

    def test_calculate_percentage_discount(self):
        discount = self.coupon.calculate_discount(Decimal('100.00'))
        self.assertEqual(discount, Decimal('20.00'))

    def test_calculate_discount_with_max(self):
        self.coupon.max_discount_amount = Decimal('15.00')
        self.coupon.save()
        discount = self.coupon.calculate_discount(Decimal('100.00'))
        self.assertEqual(discount, Decimal('15.00'))


class PromotionModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpass123',
            user_type='restaurant'
        )
        self.restaurant = Restaurant.objects.create(
            owner=self.owner,
            name='Test Restaurant',
            address='123 Test St',
            latitude=48.8566,
            longitude=2.3522,
            phone_number='+33123456789'
        )
        self.promotion = Promotion.objects.create(
            restaurant=self.restaurant,
            name='Happy Hour',
            promotion_type='percentage',
            discount_value=30,
            valid_from=timezone.now(),
            valid_until=timezone.now() + timedelta(days=7)
        )

    def test_promotion_creation(self):
        self.assertEqual(self.promotion.name, 'Happy Hour')
        self.assertEqual(self.promotion.discount_value, 30)

    def test_promotion_is_valid_now(self):
        self.assertTrue(self.promotion.is_valid_now())

    def test_promotion_inactive(self):
        self.promotion.is_active = False
        self.promotion.save()
        self.assertFalse(self.promotion.is_valid_now())
