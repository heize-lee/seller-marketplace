from django.test import TestCase
from django.urls import reverse
from .models import Product, Category

class ProductTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=10000,
            description='Test Description',
            stock_quantity=100,
            category=self.category
        )

    def test_product_list(self):
        response = self.client.get(reverse('product:product'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail(self):
        response = self.client.get(reverse('product:product_detail', args=[self.product.product_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Test Description')
