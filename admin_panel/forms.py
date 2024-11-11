from django import forms
from ekart.models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'image', 'description', 'price', 'category', 'stock_quantity', 
                  'color', 'size', 'weight', 'material', 'warranty']
