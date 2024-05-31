from django.contrib import admin
from . models import MenuItem, Category, OrderModel, Product, Cart, Customer, ReservationModel, OrderPlaced, RedemptionOption

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(ReservationModel)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','category','image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email', 'full_name', 'phone', 'points']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity','ordered_date']

@admin.register(RedemptionOption)
class RedemptionOptionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'points_required', 'image']
