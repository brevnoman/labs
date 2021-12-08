from django.contrib.auth.models import AbstractUser
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255,
                            verbose_name='Category name')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ManyToManyField(Category,
                                      verbose_name='Category',
                                      related_name='related_product')
    title = models.CharField(max_length=255,
                             verbose_name='Product title')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Product Image',
                              blank=True)
    description = models.TextField(verbose_name='Product description',
                                   null=True)
    price = models.DecimalField(max_digits=15,
                                decimal_places=2,
                                verbose_name='Product Price')

    def __str__(self):
        return self.title


class CartProduct(models.Model):

    cart = models.ForeignKey('Cart',
                             verbose_name='Cart',
                             on_delete=models.CASCADE,
                             related_name='related_products')
    product: Product = models.ForeignKey(Product,
                                         verbose_name='Product',
                                         on_delete=models.CASCADE)
    qty: int = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      verbose_name='Total Price', blank=True, null=True)

    def __str__(self):
        return f'Cart Product {self.product.title}'

    def save(self, *args, **kwargs):
        self.final_price = self.product.price * self.qty
        super().save(*args, **kwargs)
        if self.qty <= 0:
            self.delete()


class Cart(models.Model):
    owner = models.ForeignKey('Customer',
                              null=True,
                              verbose_name='Cart Owner',
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct,
                                      blank=True,
                                      related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=15,
                                      decimal_places=2,
                                      verbose_name='Total Price', null=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(AbstractUser):

    phone_number = models.CharField(max_length=20, verbose_name='Phone number', blank=True, null=True)
    address = models.CharField(max_length=255, verbose_name='Address', blank=True, null=True)
    orders = models.ManyToManyField('Order', verbose_name='Orders', related_name='related_customer', blank=True)
    def __str__(self):
        return f'Customer: {self.username}, {self.phone_number}'


class Wishlist(models.Model):
    owner = models.ForeignKey('Customer',
                              verbose_name='Wishlist Owner',
                              on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,
                                      blank=True,
                                      related_name='related_wishlist')

    def __str__(self):
        return str(self.id)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOISES = (
        (STATUS_NEW, 'New Order'),
        (STATUS_IN_PROGRESS, 'Order in progress'),
        (STATUS_READY, 'Order Ready'),
        (STATUS_COMPLETED, 'Order is completed')
    )

    BUYING_TYPE_CHOISES = (
        (BUYING_TYPE_SELF, 'Self pickup'),
        (BUYING_TYPE_DELIVERY, 'Delivery')
    )

    customer = models.ForeignKey(Customer, verbose_name='Customer', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='First Name')
    last_name = models.CharField(max_length=255, verbose_name='Last Name')
    phone = models.CharField(max_length=28, verbose_name='Phone Number')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address')
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=100,
                              verbose_name='Order Status',
                              choices=STATUS_CHOISES,
                              default=STATUS_NEW)
    buying_delivery = models.CharField(max_length=100,
                                       choices=BUYING_TYPE_CHOISES,
                                       default=BUYING_TYPE_SELF,
                                       verbose_name='Buying delivery type')
    comment = models.TextField(verbose_name='Order comment', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Order create time')
