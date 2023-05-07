from django.db import models

from sales.models.base import BaseTime
from sales.models.product import Product


class Customer(BaseTime):
    full_name = models.CharField(max_length=60, blank=True, null=True)
    number = models.CharField(max_length=14, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f'{self.full_name} {self.id} {self.number}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

class OrderItem(BaseTime):
    customer_order = models.ForeignKey(Customer, related_name='customer_order', on_delete=models.CASCADE)
    products = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    @property
    def get_cost(self):
        return self.price * self.quantity