from django.db import models

from sales.models.base import BaseTime
from sales.models.product import Product


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

class Order(BaseTime):
    order_id = models.CharField(max_length=8, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    money_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.customer.full_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    money_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.id}'

    @property
    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def get_change(self):
        change = self.money_received - self.get_cost
        return change