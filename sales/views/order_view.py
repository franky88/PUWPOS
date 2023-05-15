from sales.models.order import OrderItem, Customer
from django.shortcuts import render, redirect
from sales.forms.order_form import CustomerForm
from sales.forms.sale_form import SaleForm
from sales.addcart import Cart
from django.views.generic import ListView


def billing_information_view(request):
    cart = Cart(request)
    customers = Customer.objects.all()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        # money_received = request.POST.get('money_received')
        if form.is_valid():
            customer = form.save()
            for item in cart:
                order = OrderItem(
                    customer_order = customer,
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
    return render(request, 'pos/billing_information.html', {'form': form, 'cart': cart, 'customers': customers})


class OrderItemView(ListView):
    template_name = 'pos/order_list.html'
    model = OrderItem
    context_object_name = 'order'
    paginate_by = 15