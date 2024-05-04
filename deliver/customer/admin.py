from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Product

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','category','image']