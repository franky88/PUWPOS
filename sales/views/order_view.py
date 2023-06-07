from sales.models.order import OrderItem, Customer
from django.shortcuts import render, redirect
from sales.forms.order_form import CustomerForm
from sales.forms.sale_form import SaleForm
from sales.addcart import Cart
from django.views.generic import ListView
from django.views import View


def billing_information_view(request):
    cart = Cart(request)
    customers = Customer.objects.all().order_by('-created_at')
    sale_form = SaleForm(request.POST or None)
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
    return render(request, 'pos/billing_information.html', {'form': form, 'cart': cart, 'customers': customers, 'sale_form': sale_form})

class OrderItemView(View):
    template_name = 'pos/order_list.html'
    def get(self, request, *args, **kwargs):
        customer_order = Customer.objects.all()
        order_count = 0
        def order_count():
            order_count = OrderItem.objects.filter(costumer_order=customer_order).count()
            return order_count
        context = {'customer_order': customer_order, 'order_count': order_count()}
        return render(request, self.template_name, context)
