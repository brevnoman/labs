from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View
from mainapp.models import Product, Category, Cart, CartProduct, Wishlist
from mainapp.forms import OrderForm, CustomerCreationForm
from mainapp.utils import recalc_cart
from django.db import transaction


class AllProductsView(View):

    def get(self, request, *args, **kwargs):
        products_qs = Product.objects.all()
        return render(request,
                      'all_products.html',
                      context={'products': products_qs})


class ProductView(View):

    def get(self, request, id, *args, **kwargs):
        products_qs = Product.objects.get(id=id)
        return render(request, 'product_detail.html', context={'product': products_qs})


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        products_qs = Product.objects.all()[:8]
        return render(request,
                      'main_page.html',
                      context={
                               'products': products_qs
                      })


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main_page')
        form = CustomerCreationForm()
        return render(request,
                      'register.html',
                      context={
                          'form': form,
                      })

    def post(self, request, *args, **kwargs):
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
        return render(request, 'register.html', context={'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main_page')
        form = AuthenticationForm()
        return render(request,
                      'login.html',
                      context={
                               'form': form
                      })

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_page')
        return render(request,
                      'login.html',
                      context={
                          'form': form
                      })


def logout_user(request):
    logout(request)
    return redirect('main_page')


class CategoryView(View):
    def get(self, request, id, *args, **kwargs):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category)
        return render(request,
                      'category_products.html',
                      {
                       'products': products,
                       'id': id
                      })


class CartView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register_page')
        return render(
            request,
            'cart.html'
        )


class AddCartProductView(View):

    def post(self, request, *args, **kwargs):  # make it POST method
        id = request.POST.get('id')
        if not request.user.is_authenticated:
            return redirect('register_page')
        product = Product.objects.get(id=id)
        cart = Cart.objects.get(owner=request.user, in_order=False)
        cart_product, created = CartProduct.objects.get_or_create(
            cart=cart,
            product=product,
        )
        if created:
            cart.products.add(cart_product)
            recalc_cart(cart)
        else:
            cart_product.qty += 1
            cart_product.save()
        return redirect('cart')


class DecreaseCartProductView(View):

    def post(self, request, *args, **kwargs):
        cart = request.POST.get('cart')
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        cart_product = CartProduct.objects.get(product=product, cart=cart)
        cart_product.qty -= 1
        cart_product.save()
        return redirect('cart')


class ChangeQtyView(View):

    def post(self, request, *args, **kwargs):
        qty = int(request.POST.get('qty'))
        id = request.POST.get('id')
        cart = request.POST.get('cart')
        print(request.POST)
        product = Product.objects.get(id=id)
        cart_product = CartProduct.objects.get(product=product, cart=cart)
        cart_product.qty = qty
        cart_product.save()
        return redirect('cart')



class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register_page')
        form = OrderForm(initial={'first_name': request.user.first_name,
                                  'last_name': request.user.last_name,
                                  'phone': request.user.phone_number,
                                  'address': request.user.address
                                  })
        return render(request,
                      'checkout.html',
                      context={
                          'form': form
                      })


class MakeOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('register_page')
        form=OrderForm(request.POST or None)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = request.user
            cart = Cart.objects.get(owner=request.user, in_order=False)
            cart.in_order = True
            new_order.cart = cart
            new_order.save()
            recalc_cart(cart)
            if new_order.first_name:
                request.user.first_name = new_order.first_name
            if new_order.last_name:
                request.user.last_name = new_order.last_name
            if new_order.phone:
                request.user.phone_number = new_order.phone
            if new_order.address:
                request.user.address = new_order.address
            request.user.orders.add(new_order)
            request.user.save()
            return redirect('main_page')
        return redirect('checkout')


class WishlistView(View):

    def get(self, request, *args, **kwargs):
        wishlist = Wishlist.objects.get(owner=request.user)
        return render(request, 'wishlist.html', context={'wishlist': wishlist})


class RemoveWishView(View):

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        wishlist = Wishlist.objects.get(owner=request.user)
        wishlist.products.remove(product)
        wishlist.save()
        return redirect('wishlist')

class AddToWishlistView(View):

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        product = Product.objects.get(id=id)
        wishlist = Wishlist.objects.get(owner=request.user)
        wishlist.products.add(product)
        wishlist.save()
        return redirect('wishlist')