from django.db import models
from datetime import timezone, datetime
from django.contrib.auth.models import User

category_choices = (
    ('B', 'Beverage'),
    ('D', 'Desserts'),
    ('P', 'Pastries'),
    ('M', 'Main')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    # price = models.FloatField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    category = models.CharField(choices=category_choices, max_length=2)
    image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
class CustomizationOption(models.Model):
    product = models.ForeignKey(Product, related_name='customization_options', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    default_choice = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.title} - {self.name}"
    
class CustomizationChoice(models.Model):
    option = models.ForeignKey(CustomizationOption, related_name='choices', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)

    def __str__(self):
        return f"{self.option.name} - {self.name} (+${self.additional_price})"

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

def default_time():
    return datetime.now().time()

class ReservationModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True)
    date = models.DateField()
    time = models.TimeField(default=default_time)
    person = models.IntegerField(default=1)
    is_served = models.BooleanField(default=False)
    def __str__(self):
        return f'Reservation: {self.created_on.strftime("%b %d %I: %M %p")}'

class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, null=True)
    is_served = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
    

class OrderItem(models.Model):
    order = models.ForeignKey('OrderModel', on_delete=models.CASCADE)
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in order #{self.order.id}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customizations = models.ManyToManyField(CustomizationChoice, blank=True)

    @property
    def total_cost(self):
        base_cost = self.quantity * self.product.price
        customizations_cost = sum(c.additional_price for c in self.customizations.all())
        return base_cost + customizations_cost * self.quantity
    
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Example default value 'Pending'
    is_served = models.BooleanField(default=False)
    customizations = models.ManyToManyField(CustomizationChoice, blank=True)
   
    @property
    def total_cost(self):
        return self.quantity * self.product.price + sum(customization.additional_price for customization in self.customizations.all())
    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default_image.png",null=True, blank=True, upload_to='media/')
    
    def __str__(self):
        return self.full_name if self.full_name else "Unnamed Customer"
