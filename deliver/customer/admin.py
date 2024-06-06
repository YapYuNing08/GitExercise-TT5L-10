from django.contrib import admin
from . models import MenuItem, Category, OrderModel, Product, Cart, Customer, ReservationModel, OrderPlaced, CustomizationOption, CustomizationChoice, RedemptionOption, RedeemedItem, Review, Ad

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(ReservationModel)
admin.site.register(CustomizationOption)
admin.site.register(CustomizationChoice)

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

class CustomizationChoiceInline(admin.TabularInline):
    model = CustomizationChoice

class CustomizationOptionAdmin(admin.ModelAdmin):
    inlines = [CustomizationChoiceInline]

@admin.register(RedemptionOption)
class RedemptionOptionModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'points_required', 'image']

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

@admin.register(RedeemedItem)
class RedemptionOptionModelAdmin(admin.ModelAdmin):
    list_display = ['customer', 'option', 'date_redeemed']

@admin.register(Review)
class RedemptionOptionModelAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'rating', 'comment', 'date_created']
