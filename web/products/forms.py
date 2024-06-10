from django import forms
from PIL import Image
from io import BytesIO
from .models import Product, Category
 
class RegisterForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    
    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'description', 'stock_quantity', 'category', 'product_img']
        

    def clean_image(self):
        image = self.cleaned_data.get('product_img')
        if image:
            # 이미지 사이즈 조정
            max_size = (500, 500)
            img = Image.open(BytesIO(image.read()))
            img.thumbnail(max_size)
            img_format = img.format.lower()
            if img_format not in ['jpeg', 'jpg', 'png']:
                raise forms.ValidationError("올바른 이미지 포맷이 아닙니다. JPEG 또는 PNG 형식을 사용하세요.")
            return image
        else:
            raise forms.ValidationError("이미지를 업로드하세요.")