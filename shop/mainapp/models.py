from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()


# Create your models here.
# product
# category
# wishlist
# cart
# order
# order items


class Category(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name="Category name")
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category,
                                      verbose_name="Category",
                                      related_name="related_product")
    title = models.CharField(max_length=255,
                             verbose_name="Product title")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Product Image",
                              blank=True)
    description = models.TextField(verbose_name="Product description",
                                   null=True)
    price = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                verbose_name="Product Price")

    def __str__(self):
        return self.title


class CartProduct(models.Model):
    user = models.ForeignKey("Customer",
                             verbose_name="Customer",
                             on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart",
                             verbose_name="Cart",
                             on_delete=models.CASCADE,
                             related_name="related_products")
    product: Product = models.ForeignKey(Product,
                                         verbose_name="Product",
                                         on_delete=models.CASCADE)
    qty: int = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      verbose_name="Total Price", blank=True, null=True)

    def __str__(self):
        return f"Cart Product {self.product.title}"

    def save(self, remove=False, *args, **kwargs):
        if remove:
            self.qty -= 1
        else:
            self.qty += 1
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)
        if self.qty <= 0:
            self.delete()
        cart = Cart.objects.get(pk=self.cart.pk)
        cart.total_products = 0
        cart.save()


class Cart(models.Model):
    owner = models.ForeignKey("Customer",
                              null=True,
                              verbose_name="Cart Owner",
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,
                                      blank=True,
                                      related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      verbose_name="Total Price", null=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         all_products = self.products.all()
    #         products_count = 0
    #         products_price = 0
    #         for product in all_products:
    #             products_count += product.qty
    #             products_price += product.final_price
    #         self.total_products = products_count
    #         self.final_price = products_price
    #     super().save(*args, **kwargs)


class Customer(models.Model):
    user = models.ForeignKey(User,
                             verbose_name="User",
                             on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,
                             verbose_name="User phone number", blank=True)
    orders = models.ManyToManyField("Order", verbose_name="Customer Orders", related_name="related_customer")

    def __str__(self):
        return f"Customer: {self.user.username}"


class WishlistProduct(models.Model):
    user: Customer = models.ForeignKey(Customer,
                                       verbose_name="Customer",
                                       on_delete=models.CASCADE)
    wishlist = models.ForeignKey("Wishlist", verbose_name="Wishlist",
                                 on_delete=models.CASCADE,
                                 related_name="related_wishlist_product")
    product: Product = models.ForeignKey(Product,
                                         verbose_name="Wished Product",
                                         on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user.user.username}, wish {self.product.title}"


class Wishlist(models.Model):
    owner = models.ForeignKey("Customer",
                              verbose_name="Wishlist Owner",
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(WishlistProduct,
                                      blank=True,
                                      related_name="related_wishlist")

    def __str__(self):
        return str(self.id)


class Order(models.Model):

    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_READY = "is_ready"
    STATUS_COMPLETED = "completed"

    BUYING_TYPE_SELF = "self"
    BUYING_TYPE_DELIVERY = "delivery"

    STATUS_CHOISES = (
        (STATUS_NEW, "New Order"),
        (STATUS_IN_PROGRESS, "Order in progress"),
        (STATUS_READY, "Order Ready"),
        (STATUS_COMPLETED, "Order is completed")
    )

    BUYING_TYPE_CHOISES = (
        (BUYING_TYPE_SELF, "Self pickup"),
        (BUYING_TYPE_DELIVERY, "Delivery")
    )

    customer = models.ForeignKey(Customer, verbose_name="Customer", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="First Name")
    last_name = models.CharField(max_length=255, verbose_name="Last Name")
    phone = models.CharField(max_length=28, verbose_name="Phone Number")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address")
    cart = models.ForeignKey(Cart, verbose_name="Cart", on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100,
                              verbose_name="Order Status",
                              choices=STATUS_CHOISES,
                              default=STATUS_NEW)
    buying_delivery = models.CharField(max_length=100,
                                       choices=BUYING_TYPE_CHOISES,
                                       default=BUYING_TYPE_SELF,
                                       verbose_name="Buying delivery type")
    comment = models.TextField(verbose_name="Order comment", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name="Order create time")
