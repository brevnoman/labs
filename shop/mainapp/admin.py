from django.contrib import admin

# Register your models here.


from mainapp.models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(WishlistProduct)
admin.site.register(Wishlist)
