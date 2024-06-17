from django.test import TestCase
from django.utils import timezone
from products.models import Category, Product

class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category',
            slug='test-category',
        )

    def test_category_creation(self):
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_image_upload(self):
        # 기본적으로 category_image가 null=True, blank=True 이므로 필드가 비어 있을 수 있습니다.
        self.assertIsNone(self.category.category_image)

class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            category_name='Test Category',
            slug='test-category',
        )
        self.product = Product.objects.create(
            product_name='Test Product',
            product_price=10000,
            description='Test Description',
            stock_quantity=10,
            category=self.category,
            seller_email='test@example.com',
        )

    def test_product_creation(self):
        self.assertTrue(isinstance(self.product, Product))
        self.assertEqual(str(self.product), 'Test Product')

    def test_default_category(self):
        default_category_id = self.product.category.id
        self.assertEqual(default_category_id, self.category.id)

    def test_updated_date(self):
        old_updated_date = self.product.updated_date
        self.product.product_price = 15000
        self.product.save()
        new_updated_date = self.product.updated_date
        self.assertNotEqual(old_updated_date, new_updated_date)
        self.assertTrue(new_updated_date > old_updated_date)

    def test_product_image_upload(self):
        # 기본적으로 product_img가 null=True, blank=True 이므로 필드가 비어 있을 수 있습니다.
        self.assertIsNone(self.product.product_img)
