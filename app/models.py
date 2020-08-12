from django.db import models
from django.contrib.auth.models import AbstractUser 
from decimal import Decimal as D

CITY_CHOICES = [
        ('Harare', 'Harare'),
        ('Bulawayo', 'Bulawayo'),
    ]

class ShippingFee(models.Model):
    city = models.CharField(max_length=64, choices=CITY_CHOICES)
    amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=16, choices=[('USD', 'USD'), ('ZWL', 'ZWL')])

    def __str__(self):
        return "%s: %f%s" %(self.city, self.amount, self.currency)


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=1024, blank=True, default="")
    address_line_2 = models.CharField(max_length=1024, blank=True, default="")
    telephone_number = models.CharField(max_length=1024, blank=True, default="")
    cell_number = models.CharField(max_length=256, blank=True, default="")
    city = models.CharField(max_length=256, blank=True, default="Harare", choices=CITY_CHOICES)

    @property 
    def recent_orders(self):
        return self.order_set.exclude(status='cart').order_by('date').reverse()[:3]

    @property 
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __str__(self):
        return self.email
        #return "%s %s" % (self.first_name, self.last_name)
    
    
#singleton
class AppSettings(models.Model):
    promo_title = models.CharField(max_length=255, blank=True, default="")
    promo_message = models.TextField(blank=True, default="")
    show_banner = models.BooleanField(default=False)
    banner_image = models.ImageField()
    base_currency = models.CharField(max_length=16, default='USD')
    secondary_currency = models.CharField(max_length=16, default='ZWL')
    exchange_rate = models.FloatField(default=1.0)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SKU(models.Model):
    sku_id = models.CharField(max_length=64)
    attribute = models.CharField(max_length=255)
    value  = models.CharField(max_length=255)
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.sku_id


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=24, decimal_places=2)
    discount = models.DecimalField(max_digits=24, decimal_places=2)
    featured = models.BooleanField(default=False, blank=True, null=True)
    category = models.ForeignKey('app.Category', on_delete=models.SET_NULL, null=True)
    sales_rank = models.IntegerField(default=0)
    related_products = models.ManyToManyField('app.Product', blank=True)

    @property
    def quantity_in_stock(self):
        return sum(i.quantity for i in SKU.objects.filter(product=self))

    @property 
    def in_stock(self):
        return self.quantity_in_stock > 0

    @property
    def discounted_price(self):
        discount = self.unit_price * (self.discount / 100)
        return round(self.unit_price - discount, 2)

    def __str__(self):
        return self.name

    @property
    def primary_photo_url(self):
        if self.productimage_set.all().count() > 0:
            return self.productimage_set.all().order_by('pk').first().image.url
        
        return ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.sku_set.all().count() == 0:
            SKU.objects.create(sku_id= "PROD%s" % self.pk,
                                attribute='Basic',
                                value='Default',
                                product=self,
                                quantity=0)


class ProductImage(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return "PRODUCT (%s) IMAGE " % str(self.product)


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    show_in_navigation = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    @property
    def products(self):
        return Product.objects.filter(category__department = self)


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    parent_category = models.ForeignKey('app.Category', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('app.Department', on_delete=models.CASCADE)
    image = models.ImageField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_OPTIONS = [
        ('cart', 'cart'),
        ('order', 'order'),
        ('paid', 'paid'),
        ('processing', 'processing'),
        ('shipped', 'shipped'),
        ('received', 'received')
    ]
    date = models.DateField()
    customer = models.ForeignKey('app.customer', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=32, choices=STATUS_OPTIONS)
    shipping_address = models.TextField(blank=True, default='')
    billing_address  = models.TextField(blank=True, default='')
    currency = models.CharField(max_length=16, choices=[('USD', 'USD'), ('ZWL', 'ZWL')])
    shipping_cost = models.DecimalField(decimal_places=2, max_digits=24)
    tax = models.DecimalField(decimal_places=2, max_digits=24, default=14.5, )

    @property
    def primary_img(self):
        if self.orderitem_set.first():
            return self.orderitem_set.first().item.primary_photo_url

    def __str__(self):
        return "ORD%d" % self.id

    @property
    def subtotal(self):
        return self.total - self.tax_amount

    @property
    def tax_amount(self):
        return self.total * (self.tax /D(100.0))

    @property
    def total(self):
        return sum(i.subtotal for i in self.orderitem_set.all())

class OrderItem(models.Model):
    item =  models.ForeignKey('app.Product', on_delete=models.SET_NULL, null=True)
    sku =  models.ForeignKey('app.SKU', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    subtotal = models.DecimalField(decimal_places=2, max_digits=24)
    discount = models.DecimalField(decimal_places=2, max_digits=6)
    order = models.ForeignKey('app.Order', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s x %s" % (self.quantity, str(self.item))

class Payment(models.Model):
    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=24)
    method = models.CharField(max_length=32)
    currency = models.CharField(max_length=16)
    timestamp = models.DateTimeField(auto_now=True)
    order = models.ForeignKey('app.Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.payment_id
    

class WishlistItem(models.Model):
    product = models.ForeignKey('app.Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('app.Customer', on_delete=models.CASCADE)
    date_added = models.DateField(auto_now=True)


    def __str__(self):
        return str(self.product)



class FaqCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=64)

    def __str__(self):
        return str(self.name)


class FaqItem(models.Model):
    question = models.CharField(max_length=256)
    answer = models.TextField()
    department = models.ForeignKey('app.FaqCategory', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.question)


class OutstandingEmailConfirmation(models.Model):
    user_email = models.EmailField()
    request_id = models.CharField(max_length=255)
    

class PasswordRecoveryRequest(models.Model):
    user_email = models.EmailField()
    request_id = models.CharField(max_length=255)
