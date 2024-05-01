from django.contrib import admin
from .models import MenuItem, Category, OrderModel, OrderItem

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'total_price', 'order']  
    # Other customization options as needed

admin.site.register(OrderItem, OrderItemAdmin)
