from django.contrib import admin
from . models import MenuItem, Category, OrderModel, Product, Cart, Customer

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','category','image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'mobile', 'address']