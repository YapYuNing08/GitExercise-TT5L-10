from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Book_table

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Book_table)