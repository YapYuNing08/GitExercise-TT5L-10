from django.db import models
from datetime import timezone, datetime
from django.contrib.auth.models import User
import random
import string 

category_choices = (
    ('B', 'Beverage'),
    ('D', 'Desserts'),
    ('P', 'Pastries'),
    ('M', 'Main')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    category = models.CharField(choices=category_choices, max_length=2)
    image = models.ImageField(upload_to='product')
    quantity_sold = models.IntegerField(default=0)  # New field to track quantity sold

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
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.option.name} - {self.name} (+${self.additional_price})"

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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    customizations = models.ManyToManyField(CustomizationChoice, blank=True)

    @property
    def total_cost(self):
        base_cost = self.quantity * self.product.price
        customizations_cost = sum(c.additional_price for c in self.customizations.all())
        return base_cost + customizations_cost * self.quantity
    
    def customization_key(self):
        return ','.join(sorted(str(c.id) for c in self.customizations.all()))


class OrderPlaced(models.Model):
    FOOD_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Served', 'Served'),
    ]
    METHOD_CHOICES = [
        ('dine-in', 'dine-in'),
        ('pick-up', 'pick-up'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    food_status = models.CharField(max_length=10, choices=FOOD_STATUS_CHOICES, default='Pending')
    is_served = models.BooleanField(default=False)
    customizations = models.ManyToManyField(CustomizationChoice, blank=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='dine-in')
    table_number = models.CharField(max_length=10, null=True, blank=True)
    order_id = models.CharField(blank=True, max_length=100)
    points = models.IntegerField(default=0)

    @property
    def total_cost(self):
        return self.quantity * self.product.price + sum(customization.additional_price for customization in self.customizations.all())
    
    def __str__(self):
        return f"Order {self.id} - {self.food_status}"

    
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="default_image.png",null=True, blank=True, upload_to='media/')
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name if self.full_name else "Unnamed Customer"
    
class RedemptionOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    points_required = models.IntegerField()
    image = models.ImageField(upload_to='redemption_images/')
    review_required = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class RedeemedItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    option = models.ForeignKey(RedemptionOption, on_delete=models.CASCADE)
    date_redeemed = models.DateTimeField(auto_now_add=True)
    claimed = models.BooleanField(default=False)
    claim_code = models.CharField(max_length=10, unique=True, null=True, blank=True)

    def generate_claim_code(self):
        self.claim_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        self.save()

class Ad(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='ads/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} on {self.product}"
    
class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='additional_images')

    def _str_(self):
        return f"Additional Image for {self.product.title}"
