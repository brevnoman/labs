from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from mainapp.forms import CustomerChangeForm, CustomerCreationForm
from mainapp.models import *
from django.utils.translation import gettext_lazy as _


class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address', 'orders')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wishlist)
admin.site.register(Order)

