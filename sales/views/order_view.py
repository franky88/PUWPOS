from sales.models.order import OrderItem, Customer, Order
from sales.models.product import Product
from django.shortcuts import render, redirect, get_object_or_404
from sales.forms.order_form import CustomerForm
from sales.forms.sale_form import SaleForm
from sales.addcart import Cart
from django.views.generic import ListView
from django.views import View
import uuid

def billing_information_view(request):
    cart = Cart(request)
    cart_items = cart.__len__()
    customers = Customer.objects.all().order_by('-created_at')
    sale_form = SaleForm(request.POST or None)
    uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:12]
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if sale_form.is_valid():
            sale_obj = sale_form.save(commit=False)
            for item in cart:
                order = OrderItem(
                    customer_order = sale_obj.customer_order,
                    products = item['product'],
                    price = item['price'],
                    quantity = item['quantity'],
                    money_received = request.POST.get('money_received')
                )
                order.products.quantity -= order.quantity
                order.products.save()
                order.save()
            cart.clear()
            return redirect('sales:pos_view')
    else:
        form = CustomerForm()
    return render(request, 'pos/billing_information.html', {'form': form, 'cart': cart, 'customers': customers, 'sale_form': sale_form, 'cart_items': cart_items})

def customer_order_details(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    orders = Order.objects.filter(customer=customer)
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
