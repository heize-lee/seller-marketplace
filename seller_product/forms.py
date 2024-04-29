from django import forms
from .models import Product, Category
 
class RegisterForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'description', 'quantity', 'total_price', 'category']