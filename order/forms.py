from django.forms import ModelForm
from .models import CartItem
from main.models import Makanan

class CartItemForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity', 'product']
        '''widgets = {
            'product': forms.HiddenInput(),  # Menyembunyikan field product
        }'''
