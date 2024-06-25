from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from reviews.models import Review
from accounts.models import CustomUser
from products.models import Product
class Command(BaseCommand):  
    help = 'Add as many reviews as you want'

    def add_arguments(self, parser):
        parser.add_argument('review_cnt', type=int)

    def handle(self, *args, **options):
        review_cnt = options['review_cnt']
        if review_cnt > 0:
            user = CustomUser.objects.first()
            product = Product.objects.first()
            image_path= 'media/review_images/2024/06/21/컵.png'
            with open(image_path,'rb') as img_file:
                image_file = File(img_file)
                Review.objects.bulk_create(
                    [Review(user=user,product=product,rating=1,image=image_file,comment="Sample Text #{}".format(i)) for i in range(review_cnt)]
                )
                self.stdout.write(self.style.SUCCESS('Successfully add {} posts'.format(review_cnt)))