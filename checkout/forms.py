from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ('plans', 'full_name', 'phone_number', 'country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county')