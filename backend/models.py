from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE)
    # responsible for add/remove Products and Product Quantities or enable-disable Categories,
    # and also add/remove discounting Factor

class CustomerAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length = 100)
    pincode = models.CharField(max_length = 10)
    latitude = models.FloatField(blank = True)
    longitude = models.FloatField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

class Branch(models.Model):
    address = models.CharField(max_length = 100)
    city = models.CharField(max_length = 30)
    pincode = models.CharField(max_length = 10)
    longitude = models.FloatField(blank = True)
    latitude = models.FloatField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)

class Product(models.Model):
    id = models.CharField(max_length = 40, primary_key = True)
    description = models.CharField(max_length = 40)
    created_at = models.DateTimeField(auto_now_add = True)

class Categories(models.Model):
    id = models.CharField(max_length = 40, primary_key = True)
    description = models.CharField(max_length = 60)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

class ProductCategoryRelation(models.Model):
    product = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    category = models.ForeignKey(Categories, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class ComboProduct(models.Model):
    id = models.CharField(max_length = 50, primary_key = True)
    description = models.CharField(max_length = 100)
    is_active = models.BooleanField(default=True)
    branch = models.ForeignKey(Branch, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class ComboProductRelation(models.Model):
    combo_product = models.ForeignKey(ComboProduct, on_delete = models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class Pricing(models.Model):
    class Meta:
        unique_together = (('product', 'branch', 'unit', 'version'),)
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    unit = models.FloatField()
    version = models.CharField(max_length = 4)
    branch = models.ForeignKey(Branch, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class Storage(models.Model):
    class Meta:
        # example 100 packets of ('koramangla', 'chicken_curry_cut_small', 0.5Kg) 
        unique_together = (('branch', 'product', 'unit'),)  
    branch = models.ForeignKey(Branch, on_delete = models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete = models.DO_NOTHING)
    quantity = models.IntegerField()
    unit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    customer_address = models.ForeignKey(CustomerAddress, on_delete = models.DO_NOTHING)
    amount = models.FloatField()
    # for the time being will store as string so it can be parsable into json object
    # otherwise JSONField is suitable field 
    # order breakup will contains {'items': [obj1, obj2], net_amount: 123, 'gst': '', discount: 123, gross_amount: 12345}
    # obj1 = {'type': 'individual','discount': 0, items: [{prodcut: product_id, price: price }, 'quantity': 2]}
    # obj2 = {'type': 'combo','discount': 0, items: [{prodcut: product_id1, price: price1 }, {prodcut: product_id,2 price: price2 }, 'quantity': 1]}
    order_breakup = models.CharField(max_length = 300, default='', blank=True)  #models.JSONField()
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length = 10)
    branch  = models.ForeignKey(Branch, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

# class Discounting(models.Model):
#     pass

# class Payment(models.Model):
#     amount = models.FloatField()
#     payment_method = models.CharField(max_length=30)
#     status = models.CharField(max_length=10)