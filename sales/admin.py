from django.contrib import admin
from sales.models.product import Product, ProductCategory, ProductImage
from sales.models.order import Customer
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'price', 'best_price', 'total_best_price', 'total_cost', 'sub_total']

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)