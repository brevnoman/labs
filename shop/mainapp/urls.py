from django.urls import path
from mainapp.views import DecreaseCartProductView, AddCartProductView, CartView, MainPageView, ProductView, RegisterView, LoginView, \
    CategoryView, logout_user, AllProductsView, CheckoutView, MakeOrderView, ChangeQtyView, WishlistView, RemoveWishView, AddToWishlistView


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('registration', RegisterView.as_view(), name='register_page'),
    path('products/<slug>', ProductView.as_view(), name='product_detail_page'),
    path('sing_in', LoginView.as_view(), name='login_page'),
    path('category/<slug>', CategoryView.as_view(), name='category_products_page'),
    path('logout', logout_user, name='logout_page'),
    path('all_products', AllProductsView.as_view(), name='all_products_page'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/',AddCartProductView.as_view(), name="add_to_cart_page"),
    path('cart/remove/', DecreaseCartProductView.as_view(), name='remove_cart_product'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make_order/', MakeOrderView.as_view(), name='make_order'),
    path('change_qty/', ChangeQtyView.as_view(), name='change_qty'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('remove_from_wishlist', RemoveWishView.as_view(), name='remove_from_wishlist'),
    path('add_to_wishlist', AddToWishlistView.as_view(), name='add_to_wishlist')
]
