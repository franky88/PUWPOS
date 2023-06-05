from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from sales.forms.order_form import CustomerForm

from sales.models.product import Product
from sales.models.order import Customer, OrderItem
from sales.addcart import Cart

class POSView(View):
    template_name = 'pos_view.html'
    def get(self, request):
        products = Product.objects.all()
        customers = Customer.objects.all()
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}
        context = {
            'title': 'POS view',
            'products': products,
            'cart': cart,
            'customers': customers,
        }
        return render(request, self.template_name, context)
    
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=True)
    return redirect('sales:pos_view')

def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
    return redirect('sales:pos_view')

def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('sales:pos_view')

@require_POST
def cart_updated(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST.get('number'))
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=number, update_quantity=True)
    return redirect('sales:pos_view')

@require_POST
def stock_out(request, id):
    number = None
    cart = Cart(request)
    if request.method == 'POST':
        number = int(request.POST.get('number'))
    product = get_object_or_404(Product, id=id)
    updated_qty = product.quantity - int(request.POST.get('number'))
    cart.add(product=product, quantity=updated_qty, update_quantity=True)
    return redirect('sales:pos_view')