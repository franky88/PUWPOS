from django.contrib import admin
from sales.models.product import Product, ProductCategory, ProductImage, StockTransaction, ProductUnit, ProductWarranty
from sales.models.order import Customer, OrderItem
from import_export import resources
from import_export.fields import Field
# Register your models here.

admin.site.site_header = "PCUWant"

class ProductResource(resources.ModelResource):
    is_serial = Field()
    out_of_stock = Field()

    class Meta:
        model = Product
        export_order = ['id', 'bar_code', 'product_code', 'name', 'model', 'description', 'category', 'created_at', 'updated_at']

    def dehydrate_is_serial(self, obj):
        if obj.is_serial:
            return "Yes"
        return "No"
    def dehydrate_out_of_stock(self, obj):
        if obj.out_of_stock:
            return "Yes"
        return "No"

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'cost', 'price', 'best_price', 'total_best_price', 'total_cost', 'sub_total']

admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(StockTransaction)
admin.site.register(ProductUnit)
admin.site.register(ProductWarranty)
admin.site.register(OrderItem)