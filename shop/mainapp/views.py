from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import View
from mainapp.models import Product, Category, Customer, Cart, CartProduct


class MainView(View):
    categories = Category.objects.all()

    def get_cart(self, request):
        if request.user.is_authenticated:
            customer = self.get_customer(request)
            cart, created = Cart.objects.get_or_create(owner=customer, in_order=False)
            if created:
                cart.save()
        else:
            cart = Cart.objects.create(
                for_anonymous_user=True
            )
        return cart


    def get_customer(self, request):
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user)
            if created:
                customer.save()
            return customer


class AllProducts(MainView):
    def get(self, request, *args, **kwargs):
        cart = self.get_cart(request)
        products_qs = Product.objects.all()
        return render(request, "all_products.html",
                      {"cart": cart, "products": products_qs, "categories": self.categories})


class Products(MainView):

    def get(self, request, slug, *args, **kwargs):
        products_qs = Product.objects.get(slug=slug)
        cart = self.get_cart(request)
        return render(request, "product_detail.html",
                      {"cart": cart, "product": products_qs, "categories": self.categories})


class MainPage(MainView):
    def get(self, request, *args, **kwargs):
        products_qs = Product.objects.all()[:8]
        cart = self.get_cart(request)
        return render(request, "main_page.html",
                      context={"cart": cart, "products": products_qs, "categories": self.categories})


class RegisterPage(MainView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = UserCreationForm()
        cart = self.get_cart(request)
        return render(request, "register.html", {"cart": cart, "form": form, "categories": self.categories})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        return redirect("register_page")


class LoginPage(MainView):
    def get(self, request):
        cart = self.get_cart(request)
        if request.user.is_authenticated:
            return redirect("/")
        form = AuthenticationForm
        return render(request, "login.html", {"cart": cart, "form": form, "categories": self.categories})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
        return redirect("login_page")


class CategoryProducts(MainView):
    def get(self, request, slug, *args, **kwargs):
        cart = self.get_cart(request)
        category = Category.objects.get(slug=slug)
        category_qs = Product.objects.filter(category=category)
        return render(request, "category_products.html",
                      {"cart": cart, "products": category_qs, "slug": slug, "categories": self.categories})


def logout_user(request):
    logout(request)
    return redirect("main_page")


class CartView(MainView):

    def get(self, request, *args, **kwargs):
        cart = self.get_cart(request)
        context = {
            "cart": cart,
            "categories": self.categories
        }
        return render(request, "cart.html", context=context)


class AddToCartView(MainView):

    def get(self, request, slug, *args, **kwargs):
        cart = self.get_cart(request)
        customer = self.get_customer(request)
        product = Product.objects.get(slug=slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=customer,
            cart=cart,
            product=product,
        )
        if created:
            cart.products.add(cart_product)
        else:
            cart_product.save()
        return HttpResponseRedirect('/cart/')


class RemoveCartProduct(MainView):
    def get(self, *args, **kwargs):
        cart, slug = kwargs.get("cart"), kwargs.get("slug")
        product = Product.objects.get(slug=slug)
        cart_product = CartProduct.objects.get(product=product, cart=cart)
        cart_product.save(remove=True)
        return redirect("cart")
