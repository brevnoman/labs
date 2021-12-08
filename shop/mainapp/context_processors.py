from mainapp.models import Category, Cart, Wishlist
from mainapp.utils import recalc_cart


def cart_and_categorise(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        wishlist, created_wishlist = Wishlist.objects.get_or_create(owner=request.user)
        if created_wishlist:
            wishlist.save()
        cart, created = Cart.objects.get_or_create(owner=request.user, in_order=False)
        if created:
            cart.save()
        context = {'cart': cart, 'categories': categories, 'wishlist': wishlist}
    else:
        cart, created = Cart.objects.get_or_create(
            for_anonymous_user=True
        )
        context = {'cart': cart, 'categories': categories}
    recalc_cart(cart)
    return context


# class CartAndCategoriesMiddleware:
#     def __init__(self, get_response, *args, **kwargs):
#         self.get_response = get_response
#
#     def __call__(self, request, *args, **kwargs):
#         response = self.get_response(request)
#         return response
#
#     def process_template_response(self, request, response, *args, **kwargs):
#         if request.user.is_authenticated:
#             cart, created = Cart.objects.get_or_create(owner=request.user, in_order=False)
#             if created:
#                 cart.save()
#         else:
#             cart = Cart.objects.create(
#                 for_anonymous_user=True
#             )
#         categories = Category.objects.all()
#         recalc_cart(cart)
#         response.context_data['categories'] = categories
#         response.context_data['cart'] = cart
#         return response

# def add_curt_and_category(get_response):
#
#     def middleware(request):
#         if request.user.is_authenticated:
#             cart, created = Cart.objects.get_or_create(owner=request.user, in_order=False)
#             if created:
#                 cart.save()
#         else:
#             cart = Cart.objects.create(
#                 for_anonymous_user=True
#             )
#         categories = Category.objects.all()
#         recalc_cart(cart)
#         response = get_response(request)
#         response.context_data['categories'] = categories
#         response.context_data['cart'] = cart
#
#         return response
#     return middleware