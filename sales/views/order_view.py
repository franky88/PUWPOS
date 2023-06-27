from sales.models.order import OrderItem, Customer
from sales.models.product import Product
from django.shortcuts import render, redirect, get_object_or_404
from sales.forms.order_form import CustomerForm
from sales.forms.sale_form import SaleForm
from sales.addcart import Cart
from django.views.generic import ListView
from django.views import View
import uuid


class OrderInformationView(View):
    customer_form = CustomerForm
    sale_form = SaleForm
    template_name = 'pos/billing_information.html'
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().order_by('-created_at')
        cart = Cart(request)
        cart_items = cart.__len__()
        form = self.sale_form(initial=self.initial)
        customer_form = self.customer_form(initial=self.initial)
        context = {
            'form': form,
            'cart': cart,
            'customers': customers,
            'customer_form': customer_form,
            'sale_form': self.sale_form,
            'cart_items': cart_items
        }
        return render(request, self.template_name, context)
    def post(self, request):
        cart = Cart(request)
        sale_form = self.sale_form(request.POST or None)
        customer_form = self.customer_form(request.POST or None)
        if sale_form.is_valid():
            for item in cart:
                sale_obj = sale_form.save(commit=False)
                order = OrderItem(
                    customer = sale_obj.customer,
                    products = item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                    money_tender = sale_obj.money_tender,
                )
                order.products.quantity -= order.quantity
                order.products.save()
                order.save()
            cart.clear()
            return redirect('sales:pos_view')
        if customer_form.is_valid():
            obj = customer_form.save(commit=False)
            obj.save()
            return redirect('sales:billing_information')

def add_customer(request):
    customer_form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        if customer_form.is_valid():
            obj = customer_form.save(commit=False)
            obj.save()
            return redirect('sales:pos_view')
    else:
        customer_form = CustomerForm()
    context = {
        "title": "add customer",
        "customer_form": customer_form,
    }
    return render(request, 'pos/billing_information.html', context)


def customer_order_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = OrderItem.objects.filter(customer=customer)
    context = {
        "title": "customer order details",
        "customer": customer,
        "orders": orders
    }
    return render(request, 'pos/customer_order_details.html', context)

class OrderItemView(View):
    template_name = 'pos/order_list.html'
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = cart.__len__()
        customer = Customer.objects.all()
        context = {'customer': customer, 'cart_items': cart_items}
        return render(request, self.template_name, context)
