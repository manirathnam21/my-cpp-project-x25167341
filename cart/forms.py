# cart/forms.py
from django import forms
from .models import Order

class AddToCartForm(forms.Form):
    """Form for adding items to cart"""
    quantity = forms.IntegerField(min_value=1, initial=1, 
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 80px;'}))

class OrderForm(forms.ModelForm):
    """Form for placing an order"""
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }