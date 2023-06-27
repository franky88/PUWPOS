from django.db import models

from sales.models.base import BaseTime
from sales.models.product import Product
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import uuid


class Customer(models.Model):
    full_name = models.CharField(max_length=60, blank=True, null=True)
    number = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.full_name} {self.id} {self.number}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order_id = models.CharField(max_length=8, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    money_tender = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.id}'

    @property
    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def get_change(self):
        change = self.money_tender - self.get_cost
        return change
    
@receiver(post_save, sender=OrderItem)
def order_pro_save(sender, instance, created, *args, **kwargs):
    if created:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.order_id = uuid_code
        instance.save()