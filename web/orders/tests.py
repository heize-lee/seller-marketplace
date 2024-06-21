from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Product, Category
from cart.models import Cart
from datetime import date

class OrderListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='Password123!',
            phone_number='+821012341234',
            role='buyer'
        )
        self.client.login(username='testuser@example.com', password='Password123!')
        
        self.category = Category.objects.create(
            category_name='Test Category',
            slug='test-category',
        )
        
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=10000,
            stock_quantity=10,
            description='Test Description',
            category=self.category,
            seller_email='test@example.com',
            product_img='https://via.placeholder.com/148x128'
        )
        
        self.cart1 = Cart.objects.create(
            user=self.user,
            product=self.product,
            amount=2,
            total_price=20000,
            payment_total_price=20000
        )

        self.cart2 = Cart.objects.create(
            user=self.user,
            product=self.product,
            amount=3,
            total_price=30000,
            payment_total_price=30000
        )
        
        self.order1 = Order.objects.create(
            user=self.user,
            product=self.product,
            cart=self.cart1,
            order_number=1001,
            amount=2,
            total_price=20000,
            payment_total_price=20000,
            order_date=date(2024, 6, 19)
        )
        
        self.order2 = Order.objects.create(
            user=self.user,
            product=self.product,
            cart=self.cart2,
            order_number=1002,
            amount=3,
            total_price=30000,
            payment_total_price=30000,
            order_date=date(2024, 6, 20)
        )

    def test_order_list_view(self):
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order_list.html')
        self.assertContains(response, 'Order #1001')
        self.assertContains(response, 'Order #1002')
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '20,000원')
        self.assertContains(response, '30,000원')
