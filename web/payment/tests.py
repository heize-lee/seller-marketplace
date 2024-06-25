from django.test import TestCase, Client
from unittest.mock import patch, MagicMock
from datetime import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
import os
import json
from cart.models import Cart
from products.models import Product, Category
from orders.models import Order, OrderItems
from .models import Payment


# Create your tests here.
User = get_user_model()

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            password='12345',
            email='testuser@example.com',
            phone_number='1234567890'
        )
        self.category = Category.objects.create(category_name='Category 1', slug='category-1')

        self.product1 = Product.objects.create(product_name='Product 1', category=self.category, product_price=10000, stock_quantity=10, description='Description 1')
        self.product2 = Product.objects.create(product_name='Product 2', category=self.category, product_price=20000, stock_quantity=20, description='Description 2')
        
        Cart.objects.create(user=self.user, product=self.product1, amount=1, total_price=10000)
        Cart.objects.create(user=self.user, product=self.product2, amount=2, total_price=40000)
        
        self.client.login(email='testuser@example.com', password='12345')

    @patch('payment.views.requests.post')  
    def test_kakao_payment(self, mock_post):
        # 1.1 kakaoPay api 페이지를 가져온다 
        response = self.client.get(reverse('payment:kakao_payment'))  
        # 1.2 정상적으로 페이지가 로드된다.
        # 1.3 페이지 타이틀은 'kakaoPay'이다.
        self.assertContains(response, 'kakaoPay')

        # Mock을 사용하여 내부에서 Api결제가 이루어진다
        
        # 2.3 결제가 완료되면 payment 테이블에 저장된다 
        # user, payment_uuid, pay_method, pay_date, pay_totoal_price, pay_nobank_user, pay_nobank, pay_confirm
        # 2.4 order 테이블과 order_items에도 저장된다
        # 
    
        self.assertEqual(response.status_code, 200)
        # kakaoPay 
        # 2.1 order페이지에서 주문정보가 전달된다 
        # 2.2 orderName, 금액, 유저
        self.assertIn('storeId', response.context)
        self.assertIn('channelKey', response.context)
        self.assertIn('cart', response.context)
        self.assertIn('orderName', response.context)
        self.assertEqual(response.context['orderName'], 'Product 1 외 1건')

    @patch('payment.views.requests.post')  # 적절한 경로로 변경 필요
    def test_handle_kakao_payment(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'paymentId': '123456789'
        }

        data = {
            'paymentId': '123456789'
        }
        # 서버에서 코드200을 반환
        response = self.client.post(reverse('payment:handle_kakao_payment'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True})

        # payment테이블에 저장
        payment = Payment.objects.last()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.payment_uuid, '123456789')
        self.assertEqual(payment.pay_total_price, 80000)
        self.assertTrue(payment.pay_confirm)

        # order테이블에 저장
        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.payment, payment)
        self.assertEqual(order.amount, 1)
        self.assertEqual(order.total_price, 10000)
        self.assertEqual(order.payment_total_price, 80000)
        self.assertEqual(len(Order.objects.filter(user=self.user)), 1)

        # OrderItems테이블에 저장
        order_items = OrderItems.objects.filter(order=order)
        self.assertEqual(len(order_items), 2)

        # cart테이블 삭제
        cart = Cart.objects.filter(user=self.user)
        self.assertEqual(len(cart), 0)



        # 1.1 kakaoPay api 페이지를 가져온다 
        # 1.2 정상적으로 페이지가 로드된다.
        # 1.3 페이지 타이틀은 'kakaoPay'이다.
        # Mock을 사용하여 내부에서 Api결제가 이루어진다
        
        # kakaoPay 
        # 2.1 order페이지에서 주문정보가 전달된다 
        # 2.2 orderName, 금액, 유저
        
        # 2.3 결제가 완료되면 payment 테이블에 저장된다 
        # user, payment_uuid, pay_method, pay_date, pay_totoal_price, pay_nobank_user, pay_nobank, pay_confirm
        # 2.4 order 테이블과 order_items에도 저장된다
        # 
    