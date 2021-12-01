from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
# product
# category
# wishlist
# cart
# order
# order items


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Product title")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Product Image", blank=True)
    description = models.TextField(verbose_name="Product description", null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Product Price")

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    user = models.ForeignKey("Customer", verbose_name="Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Cart", on_delete=models.CASCADE, related_name="related_products")
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Price")

    def __str__(self):
        return f"Cart Product {self.content_object.name}"


class Cart(models.Model):

    owner = models.ForeignKey("Customer", verbose_name="Cart Owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Price")

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user: User = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="User phone number")

    def __str__(self):
        return "Customer:", self.user.first_name, self.user.last_name


class WishlistProduct(models.Model):

    user = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE)
    cart = models.ForeignKey("Wishlist", verbose_name="Cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Wished Product", on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user.username}, wish {self.content_object.title}"


class Wishlist(models.Model):

    owner = models.ForeignKey("Customer", verbose_name="Wishlist Owner", on_delete=models.CASCADE)
    products = models.ManyToManyField(WishlistProduct, blank=True)

    def __str__(self):
        return str(self.id)
