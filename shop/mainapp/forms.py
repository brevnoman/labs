from django import forms
from mainapp.models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            "first_name", "last_name", "phone", "address", "comment", "buying_delivery"
        )
