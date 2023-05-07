from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from sales.models.product import Product
from sales.models.order import Customer
from sales.addcart import Cart

class POSView(View):
    def get(self, request):
        products = Product.objects.all()
        customers = Customer.objects.all()
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form'] = {'quantity': item['quantity'], 'update': True}
        context = {
            'products': products,
            'cart': cart,
            'customers': customers,
        }
        template_name = 'pos_view.html'
        return render(request, template_name, context)
    
def cart_add(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=1)
    return redirect('sales:pos_view')

def cart_remove(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.remove(product)
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