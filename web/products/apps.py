from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):  #signals.py 이용해서 상품 삭제되면 이미지파일도 함께 삭제
        import products.signals

