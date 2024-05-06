from django.db import models
from datetime import datetime, date

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ManyToManyField('Category', related_name='item')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ReservationModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True)
    date = models.DateField()
    person = models.IntegerField(default=1)
    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, null=True)
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    
# class Customer(models.Model):
#     name=models.CharField(max_length=50, null=True)
#     phone=models.CharField(max_length=50, null=True)
#     email=models.EmailField()
#     date_created=models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     CATEGORY=(
#         ('Dine in','Dine in'),
#         ('Takeaway','Takeaway'),
#     )
#     name=models.CharField(max_length=50, null=True)
#     price=models.FloatField()
#     category=models.CharField(max_length=50, null=True, choices=CATEGORY)
#     description=models.CharField(max_length=200, null=True, blank=True)
#     date_created=models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return self.name

# class Order(models.Model):
#     STATUS=(
#         ('Pending','Pending'),
#         ('Served','Served'),
#     )

    # customer=models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL())
    # product=models.ForeignKey(Product,null=True, on_delete=models.SET_NULL())
    # date_created=models.DateTimeField(auto_now_add=True, null=True)
    # status=models.CharField(max_length=50, null=True, choices=STATUS)
