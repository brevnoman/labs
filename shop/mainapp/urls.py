from django.urls import path
from mainapp.views import RemoveCartProduct, AddToCartView, CartView, MainPage, Products, RegisterPage, LoginPage, \
    CategoryProducts, logout_user, AllProducts, CheckoutView, MakeOrderView

urlpatterns = [
    path("", MainPage.as_view(), name="main_page"),
    path("registration", RegisterPage.as_view(), name="register_page"),
    path("products/<slug>", Products.as_view(), name="product_detail_page"),
    path("sing_in", LoginPage.as_view(), name="login_page"),
    path("category/<slug>", CategoryProducts.as_view(), name="category_products_page"),
    path("logout", logout_user, name="logout_page"),
    path("all_products", AllProducts.as_view(), name="all_products_page"),
    path("cart/", CartView.as_view(), name="cart"),
    path("add-to-cart/<slug>/", AddToCartView.as_view(), name="add_to_cart_page"),
    path("cart/remove/<cart>/<slug>", RemoveCartProduct.as_view(), name="remove_cart_product"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("make_order/", MakeOrderView.as_view(), name="make_order"),
]
