from django import forms
from .models import Product
 
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'quantity', 'total_price']