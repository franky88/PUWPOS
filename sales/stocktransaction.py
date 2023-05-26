from decimal import Decimal
from django.conf import settings

from sales.models.product import Product, StockTransaction


class Stock(object):
    quantity = 0
    product_id = ""
    bar_code = ""
    name = ""
    model = ""
    description = ""
    cost = 0.00
    products = Product.objects.all()
    def __init__(self, request):
        for product in self.products:
            self.product_id = product.id
            self.quantity = int(product.quantity)
            self.bar_code = product.bar_code
            self.name = product.name
            self.model = product.model
            self.description = product.description
            self.cost = int(product.cost)
            print("product", self.product_id, self.name, self.model, self.description)

    def add_new_stock(self, quantity=1, is_new_stock=False):
        if is_new_stock:
            stock_transaction = StockTransaction(
                quantity = quantity,
            )
            stock_transaction.save()

    def update_stock(self, stock, quantity=1, is_new_stock=False):
        if not is_new_stock:
            stock = str(self.product_id)
            stock_transaction = StockTransaction(
                id = stock,
                # stock.stock.quantity += quantity,
            )
            stock_transaction.save()

    def update_stock_quantity(self, request, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if update_quantity:
            product = Product(
                id = product_id,
                user = request.user,
                quantity = quantity,
            )
            product.save()