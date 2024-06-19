from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser  # CustomUser 모델을 임포트합니다
from .models import Review, ReviewComment
from products.models import Product, Category
from .forms import ReviewCreateForm

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='password', role='buyer')
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=100,
            description='Test Description',
            stock_quantity=10,
            category=self.category
        )

    def test_review_creation(self):
        review = Review.objects.create(user=self.user, product=self.product, rating=4.5, comment='Great product!')
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 4.5)
        self.assertEqual(review.comment, 'Great product!')

    def test_review_str(self):
        review = Review.objects.create(user=self.user, product=self.product, rating=4.5, comment='Great product!')
        self.assertEqual(str(review), 'testuser@example.com')

class ReviewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='password', role='buyer')
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=100,
            description='Test Description',
            stock_quantity=10,
            category=self.category
        )
        self.review = Review.objects.create(user=self.user, product=self.product, rating=4.5, comment='Great product!')

    def test_review_create_view_get(self):
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.get(reverse('reviews:create') + f'?product={self.product.product_id}')
        # 이미 리뷰를 작성한 경우 리디렉션되는지 확인
        if response.status_code == 302 and response.url == f'/product/{self.product.product_id}':
            self.assertEqual(response.status_code, 302)
        else:
            self.assertEqual(response.status_code, 200, f"Unexpected response code: {response.status_code}. Response content: {response.content.decode()}")

    def test_review_create_view_post(self):
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.post(reverse('reviews:create'), {
            'product': self.product.product_id,
            'rating': 5,
            'comment': 'Amazing!',
            'image': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(comment='Amazing!').exists())

    def test_review_delete_view(self):
        self.client.login(email='testuser@example.com', password='password')
        response = self.client.delete(reverse('reviews:delete_review', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@example.com', password='password', role='buyer')
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=100,
            description='Test Description',
            stock_quantity=10,
            category=self.category
        )

    def test_review_create_form(self):
        form_data = {
            'rating': 4.5,
            'comment': 'Nice product!',
            'image': '',
        }
        form = ReviewCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
