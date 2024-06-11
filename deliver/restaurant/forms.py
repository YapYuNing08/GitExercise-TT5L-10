from django import forms
from customer.models import OrderPlaced

class FoodStatusForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['food_status']