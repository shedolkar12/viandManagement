from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)

class Admin(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE)
    # responsible for add/remove Meat Quantities or enable-disable Categories, add/remove
    # discounting Factor

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

class Meat(models.Model):
    id = models.CharField(max_length = 40, primary_key = True)
    description = models.CharField(max_length = 40)
    created_at = models.DateTimeField(auto_now_add = True)

class Categories(models.Model):
    category = models.CharField(max_length=40, primary_key = True)
    description = models.CharField(max_length = 60)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)

class ComboMeat(models.Model):
    id = models.CharField(max_length = 50, primary_key = True)
    description = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)

class ComboMeatRelation(models.Model):
    combomeat = models.ForeignKey(ComboMeat, on_delete = models.DO_NOTHING)
    meat = models.ForeignKey(Meat, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class MeatCategoryRelationShip(models.Model):
    meat = models.ForeignKey(Meat, on_delete = models.DO_NOTHING)
    category = models.ForeignKey(Categories, on_delete = models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add = True)

class Pricing(models.Model):
    class Meta:
        unique_together = (('meat', 'unit', 'version'),)
    price = models.FloatField()
    meat = models.ForeignKey(Meat, on_delete=models.DO_NOTHING)
    unit = models.FloatField()
    version = models.CharField(max_length = 4)
    created_at = models.DateTimeField(auto_now_add = True)

class Storage(models.Model):
    class Meta:
        # example 100 packets of ('koramangla', 'chicken_curry_cut_small', 0.5Kg) 
        unique_together = (('branch', 'meat', 'unit'),)  
    branch = models.ForeignKey(Branch, on_delete = models.DO_NOTHING)
    meat = models.ForeignKey(Meat, on_delete = models.DO_NOTHING)
    quantity = models.IntegerField()
    unit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    customer = models.ForeignKey(Customer, on_delete = models.DO_NOTHING)
    amount = models.FloatField()
    # for the time being will store as string so it can be parsable
    amount_breakup = models.CharField(max_length = 200)  #models.JSONField()
    # payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length = 10)
    created_at = models.DateTimeField(auto_now_add = True)

# class Discounting(models.Model):
#     pass

# class Payment(models.Model):
#     amount = models.FloatField()
#     payment_method = models.CharField(max_length=30)
#     status = models.CharField(max_length=10)