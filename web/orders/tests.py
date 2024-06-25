# orders/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from products.models import Product, Category
from cart.models import Cart
from accounts.models import DeliveryAddress
from orders.models import Order
from unittest import mock

User = get_user_model()


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='james@seller.com', password='12345', phone_number="+821045678910")
        self.client.login(email='james@seller.com', password='12345')
        image = SimpleUploadedFile(name='test_image.jpg',
                                   content=b'\x00\x01\x02\x03',
                                   content_type='image/jpeg')

        self.category = Category.objects.create(category_name='Test Category',)
        self.product1 = Product.objects.create(
            product_name='Test Product1',
            product_price=100,
            stock_quantity = 30,
            category=self.category,
            product_img=image,
        )
        self.product2 = Product.objects.create(
            product_name='Test Product2',
            product_price=100,
            stock_quantity = 30,
            category=self.category,
            product_img=image,
        )
        self.direct_purchase_product = Product.objects.create(
            product_name='Direct Purchase Product',
            product_price=100,
            stock_quantity=10,
            category=self.category,
            product_img=image,
        )
        self.cart1 = Cart.objects.create(user=self.user, product=self.product1, amount=1, total_price=100)
        self.cart2 = Cart.objects.create(user=self.user, product=self.product2, amount=2, total_price=200)

        self.delivery_address = DeliveryAddress.objects.create(
            user=self.user,
            recipient='Test Recipient',
            phone_number='01012345678',
            destination='Test Destination',
            postal_code='12345',
            address='Test Address',
            detail_address='Test Detail Address',
            is_default=True,
        )

    def test_order_page_load(self):
        # 1.1 order 페이지를 가져온다.
        response = self.client.get(reverse('orders:orders'))
        
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        
        # 1.3 페이지 타이틀은 'Order'이다.
        self.assertContains(response, 'Order')

    def test_no_default_delivery_address(self):
        # 2.1 배송정보에 기본 배송지가 없다면
        DeliveryAddress.objects.filter(user=self.user).delete()
        
        response = self.client.get(reverse('orders:orders'))
        self.assertEqual(response.status_code, 200)
        
        # 2.2 '등록된 배송지가 없습니다' 메시지가 보인다.
        self.assertContains(response, '등록된 배송지가 없습니다')
        self.assertContains(response, '배송지 추가하기 버튼을 눌러 주소를 입력해주세요')
        self.assertContains(response, '배송지 추가하기')

    def test_order_info_from_cart(self):
        # 3.1 카트에 2개가 담겨 있다면
        
        response = self.client.get(reverse('orders:orders'))
        self.assertEqual(response.status_code, 200)
        
        # 3.2 order 페이지를 새로고침 했을 때
        # 3.3 주문정보 헤더는 주문정보(카트의 length)와 카트에 담긴 object 각각의 
        #     product.product_img.url, product.product_name, product.product_price, amount, total_price가 존재한다
        self.assertContains(response, '주문정보(2)')
        self.assertContains(response, self.cart1.product.product_name)
        self.assertContains(response, self.cart1.product.product_price)
        self.assertContains(response, self.cart1.product.product_img)
        self.assertContains(response, self.cart1.amount)
        self.assertContains(response, self.cart1.total_price)
        self.assertContains(response, self.cart2.product.product_name)
        self.assertContains(response, self.cart2.product.product_price)
        self.assertContains(response, self.cart2.product.product_img)
        self.assertContains(response, self.cart2.amount)
        self.assertContains(response, self.cart2.total_price)
        self.assertContains(response, '1개')
        self.assertContains(response, '2개')
        self.assertContains(response, 'total_price')
    
    def test_order_info_direct_purchase(self):
        # 3.4 product_detail에서 바로구매로 order를 넘어올 때 
        response = self.client.get(reverse('orders:orders') + '?detail=true&product_id={}&cnt=1&total_price=100'.format(self.direct_purchase_product.pk))
        self.assertEqual(response.status_code, 200)
        # 3.5 order 페이지를 새로고침 했을 때 
        self.assertContains(response, 'Direct Purchase Product')
        self.assertContains(response, self.direct_purchase_product.product_name)
        self.assertContains(response, self.direct_purchase_product.product_price)
        # quantity
        self.assertContains(response, '10')
        # total_price
        self.assertContains(response, 'total_price')
    
    def test_payment_info(self):
        # 4.1 결제 정보에 작품 금액과 최종결제금액은 
        response = self.client.get(reverse('orders:orders'))
        self.assertEqual(response.status_code, 200)

        
        # 4.2 카트에 담긴 목록의 총합 / 바로구매일 경우 상품 수량만큼의 총합
        self.assertContains(response, 'payment_total_price')
        self.assertContains(response, self.cart1.total_price)
    
    def test_payment_method(self):
        # 4.3 결제수단(카카오페이 / 토스페이) 선택 시 
        # 4.4 결제하기는 해당 결제수단에 Api로 연결된다
        pass
    
    def test_payment_method_kakao(self):
        response_kakao = self.client.get(reverse('payment:kakao_payment'))
        self.assertEqual(response_kakao.status_code, 200)  

    def test_payment_method_toss(self):
        response_toss = self.client.get(reverse('payment:toss_payment'))
        self.assertEqual(response_toss.status_code, 200)  

    



        # 1.1 order 페이지를 가져온다.
        # 1.2 정상적으로 페이지가 로드된다.
        # 1.3 페이지 타이틀은 'Order'이다.
        
        
        # 배송지정보
        # 2.1 배송정보에 기본 배송지가 없다면 
        # 2.2 '등록된 배송지가 없습니다'  '배송지 추가하기 버튼을 눌러 주소를 입력해 주세요'  '배송지 추가하기'버튼이 보인다

        # 주문정보
        # 카트에서 주문하기 / product_detail페이지에서 바로구매
        # 3.1 카트에 2개가 담겨 있다면 
        # 3.2 order 페이지를 새로고침 했을 때 
        # 3.3 주문정보 헤더는 주문정보(카트의 length)와 카트에 담긴 object 각각의 
        #     product.product_img.url, product.product_name, product.product_price, amount, total_price가 존재한다
        # 3.4 product_detail에서 바로구매로 order를 넘어올 때 
        # 3.5 order 페이지를 새로고침 했을 때 
        # 3.6 주문정보에 담긴 product의 product_name,product_price,quantity,total_price가 존재한다
        # 3.7 주문정보 목록 삭제
        # 
        # 결제정보
        # 4.1 결제 정보에 작품 금액과 최종결제금액은 
        # 4.2 카트에 담긴 목록의 총합 / 바로구매일 경우 상품 수량만큼의 총합
        # 4.3 결제수단(카카오페이 / 토스페이) 선택 시 
        # 4.4 결제하기는 해당 결제수단에 Api로 연결된다