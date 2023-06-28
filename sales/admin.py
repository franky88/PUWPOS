from django.contrib import admin
from sales.models.product import Product, ProductCategory, ProductImage, StockTransaction
from sales.models.order import Customer
from import_export import resources
# Register your models here.

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'price', 'best_price', 'total_best_price', 'total_cost', 'sub_total']

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(StockTransaction)