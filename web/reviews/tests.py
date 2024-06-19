from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Product, Category
from reviews.models import Review

class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='testuser@example.com', password='password', phone_number='+1234567890'
        )
        cls.category = Category.objects.create(category_name='Test Category', slug='test-category')
        cls.product = Product.objects.create(
            product_name='Test Product', 
            product_price=100, 
            description='Test Description', 
            stock_quantity=10, 
            category=cls.category,
        )
    
    def test_review_creation(self):
        review = Review.objects.create(user=self.user, product=self.product, rating=4, comment='Great product!')
        self.assertEqual(review.__str__(), str(self.user))

    def test_review_str(self):
        review = Review.objects.create(user=self.user, product=self.product, rating=4, comment='Great product!')
        self.assertEqual(str(review), str(self.user))

class ReviewViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(category_name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=100,
            description='Test Description',
            stock_quantity=10,
            category=self.category
        )
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com', password='password', phone_number='+1234567890', role='buyer'
        )
        self.client.login(email='testuser@example.com', password='password')

    def test_review_create_view_get(self):
        response = self.client.get(reverse('reviews:create') + f'?product={self.product.pk}')
        self.assertEqual(response.status_code, 200)

    def test_review_create_view_post(self):
        response = self.client.post(reverse('reviews:create'), {
            'product': self.product.pk,
            'rating': 5,
            'comment': 'Great product!'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('처리완료', response.content.decode())

    def test_review_delete_view(self):
        review = Review.objects.create(user=self.user, product=self.product, rating=5, comment='Great product!')
        response = self.client.delete(reverse('reviews:delete_review', args=[review.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('리뷰가 삭제되었습니다.', response.json().get('success'))

# Run the tests
if __name__ == '__main__':
    TestCase.main()
