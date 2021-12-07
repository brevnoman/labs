from mainapp.models import Category, Cart
from mainapp.utils import recalc_cart


def cart_and_categorise(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(owner=request.user, in_order=False)
        if created:
            cart.save()
    else:
        cart = Cart.objects.create(
            for_anonymous_user=True
        )
    categories = Category.objects.all()
    recalc_cart(cart)
    return{'cart': cart, 'categories': categories}


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