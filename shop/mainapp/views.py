from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from mainapp.models import Product, Category
from mainapp.mixins import CategoryContextMixin

# def all_product(request):
#     products_qs = Product.objects.all()
#     return render(request, "all_products.html", context={"products": products_qs})
class MainView(View):
    categories = Category.objects.all()


class AllProducts(MainView):
    def get(self, request, *args, **kwargs):
        products_qs = Product.objects.all()
        return render(request, "all_products.html", {"products": products_qs, "categories": self.categories})


# def products(request, slug):
#     products_qs = Product.objects.get(slug=slug)
#     return render(request, "product_detail.html", context={"product": products_qs})

class Products(MainView):

    def get(self, request, slug, *args, **kwargs):
        products_qs = Product.objects.get(slug=slug)
        return render(request, "product_detail.html", {"product": products_qs, "categories": self.categories})


# def main_page(request):
#     products_qs = Product.objects.all()[:8]
#     categories_qs = Category.objects.all()
#     return render(request, "main_page.html", context={"categories": categories_qs, "products": products_qs})

class MainPage(MainView):
    def get(self, request, *args, **kwargs):
        products_qs = Product.objects.all()[:8]
        categories_qs = Category.objects.all()
        return render(request, "main_page.html", context={"products": products_qs, "categories": self.categories})


# def register_page(request):
#     if request.user.is_authenticated:
#         return redirect("/")
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("/")
#     form = UserCreationForm()
#     return render(request, "register.html", context={"form": form})


class RegisterPage(MainView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = UserCreationForm()
        return render(request, "register.html", {"form": form, "categories": self.categories})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
        return render(request, "register.html", {"form": form, "categories": self.categories})


# def login_page(request):
#     if request.user.is_authenticated:
#         return redirect("/")
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("/")
#     form = AuthenticationForm
#     return render(request, "login.html", context={"form": form})


class LoginPage(MainView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = AuthenticationForm
        return render(request, "login.html", {"form": form, "categories": self.categories})
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

# def category_products(request, slug):
#     category = Category.objects.get(slug=slug)
#     category_qs = Product.objects.filter(category=category)
#     return render(request, "category_products.html", context={"products": category_qs, "slug": slug})


class CategoryProducts(MainView):
    def get(self, request, slug, *args, **kwargs):
        category = Category.objects.get(slug=slug)
        category_qs = Product.objects.filter(category=category)
        return render(request, "category_products.html", {"products": category_qs, "slug": slug, "categories": self.categories})


def logout_user(request):
    logout(request)
    return redirect("main_page")


# class AllProducts(MainView):
#     def get(self, request, *args, **kwargs):
