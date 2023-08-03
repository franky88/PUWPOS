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
            serial = request.POST.get('serial')
            for item in cart:
                sale_obj = sale_form.save(commit=False)
                order_item = OrderItem(
                    customer = sale_obj.customer,
                    products = item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                    money_tender = sale_obj.money_tender,
                    serial_number = serial
                )
                order_item.products.quantity -= order_item.quantity
                order_item.products.save()
                order_item.save()
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

class OrderListView(View):
    template_name = 'pos/order_list_view.html'
    def get(self, request):
        cart = Cart(request)
        cart_items = cart.__len__()

        orders = OrderItem.objects.filter(is_confirmed=False)
        context = {
            "title": "unconfired orders",
            "orders": orders
        }
        return render(request, self.template_name, context)