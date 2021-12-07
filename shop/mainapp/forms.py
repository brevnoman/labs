from django import forms
from mainapp.models import Order, Customer
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'comment', 'buying_delivery'
        )


class CustomerCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Customer
        fields = ('username', 'email', 'phone_number', 'address')


class CustomerChangeForm(UserChangeForm):

    class Meta:
        model = Customer
        fields = '__all__'


class DecreaseProductForm(forms.Form):
    cart = forms.CharField(max_length=255)
    slug = forms.CharField(max_length=255)


class AddProductForm(forms.Form):
    slug = forms.CharField(max_length=255)