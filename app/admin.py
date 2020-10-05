from django.contrib import admin
from django.contrib.auth.models import Group
from app.models import *
# Register your models here.

admin.site.site_header = "Nomie's Collection"
admin.site.site_title = "Nomie's Collection"
admin.site.register(Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display =['name', 'discount' , 'featured' , 'unit_price' , 'category']
admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)
admin.site.register(SKU)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'image']

admin.site.register(Department, DepartmentAdmin)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'parent_category']

admin.site.register(Category, CategoryAdmin)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['status', 'customer', 'billing_address']

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
     list_display = ['item','quantity', 'order']

admin.site.register(OrderItem, OrderItemAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'amount', 'method', 'timestamp', 'order']
admin.site.register(Payment, PaymentAdmin)
admin.site.register(WishlistItem)

class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ['name','description']
admin.site.register(FaqCategory, FaqCategoryAdmin)
class FaqItemAdmin(admin.ModelAdmin):
    list_display = ['question','department']

admin.site.register(FaqItem, FaqItemAdmin)
admin.site.register(AppSettings)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['name','symbol']
admin.site.register(Currency, CurrencyAdmin)

class CurrencyExchangeAdmin(admin.ModelAdmin):
    list_display = ['date', 'rate']

admin.site.register(CurrencyExchange, CurrencyExchangeAdmin)
admin.site.unregister(Group)






