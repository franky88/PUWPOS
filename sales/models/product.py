import uuid
from django.db import models
from sales.models.base import BaseTime
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from import_export import resources


class ProductWarranty(models.Model):
    name = models.CharField(max_length=100, default="6 months")
    date_purchased = models.DateTimeField(blank=True, null=True)
    warranty_duration = models.IntegerField(default=180)

    def __str__(self):
        return self.name
    
    @property
    def item_warranty_duration(self):
        warranty = self.date_purchased.day + self.warranty_duration
        return warranty
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=100, default="Memories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

class Product(BaseTime):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    product_code = models.CharField(max_length=13, unique=True, blank=True)
    bar_code = models.CharField(max_length=13, unique=True, blank=True)
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.FloatField(default=0)
    price_margin = models.FloatField(default=0.25)
    price_discount = models.FloatField(default=0.00)
    price = models.FloatField(default=0.00, verbose_name="SRP")
    quantity = models.PositiveIntegerField(default=1)
    is_serial = models.BooleanField(default=False, verbose_name="with serial?")
    out_of_stock = models.BooleanField(default=False)
    product_warranty = models.ForeignKey(ProductWarranty, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        name = "(%s) - %s - %s" % (self.bar_code, self.name, self.model)
        return name
    
    @property
    def sub_total(self):
        subtotal = self.price * self.quantity
        return subtotal
    
    @property
    def best_price(self):
        discount = float(self.price) - float(self.cost)
        price = (discount - (discount * self.price_discount)) + float(self.cost)
        return price
    
    @property
    def total_cost(self):
        totalcost = self.cost * self.quantity
        return totalcost
    
    @property
    def total_best_price(self):
        total = self.best_price * self.quantity
        return total
    
    @property
    def discount(self):
        if not self.price - self.best_price == 0:
            disc = ((self.price - self.best_price)/self.price)*100
            return disc


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product-image/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        img = self.image_name
        return img

class StockTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cost = models.FloatField(default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = "%s - %s" % (self.stock.name, self.stock.model)
        return name
    
    @property
    def stock_cost(self):
        cost = self.quantity * self.cost
        return cost

# class ProductResource(resources.ModelResource):
#     class Meta:
#         model = Product
#         import_id_fields = ["bar_code", "name", "model", "description", "category", "cost", "price_margin", "price_discount", "price", "quantity", "is_serial", "product_warranty"]
#         skip_unchanged = True
#         use_bulk = True

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, *args, **kwargs):
    if instance.product_code == "":
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:12]
        instance.product_code = uuid_code
    if instance.price == 0.00 or instance.price < instance.cost:
        price = float(instance.cost) * (1 + instance.price_margin)
        instance.price = price
    if instance.quantity <= 1:
        instance.out_of_stock = True
    else:
        instance.out_of_stock = False