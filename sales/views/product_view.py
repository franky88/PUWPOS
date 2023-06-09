from django.shortcuts import render, redirect, get_object_or_404
from sales.forms.product_form import ProductForm, ProductCategoryForm
from sales.forms.stock_form import StockForm
from sales.models.product import Product, StockTransaction, ProductCategory
from sales.addcart import Cart
from django.views import View
from sales.stocktransaction import Stock
from django.views.generic import CreateView
from django.urls import reverse_lazy


class ProductView(View):
    template_name = 'product_list.html'
    form_class = ProductForm
    category_form_class = ProductCategoryForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = cart.__len__()
        form = self.form_class(initial=self.initial)
        category_form = self.category_form_class(initial=self.initial)
        products = Product.objects.all().order_by('-updated_at', '-created_at')
        categories = ProductCategory.objects.all()
        context = {
            'products': products,
            'form': form,
            'categoryform': category_form,
            'categories': categories,
            'cart_items': cart_items
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        category_form = self.category_form_class(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('sales:product_list')
        if category_form.is_valid():
            obj = category_form.save(commit=False)
            obj.save()
            return redirect('sales:product_list')
        context = {
            "form": form,
            "categoryform": category_form
        }
        return render(request, self.template_name, context)

def add_to_cart(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=True)
    return redirect('sales:product_list')

class StockView(View):
    template_name = 'stock/stock_list.html'
    form_class = StockForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = cart.__len__()
        form = self.form_class(initial=self.initial)
        stocks = StockTransaction.objects.all().order_by('-timestamp')[:5]
        products = Product.objects.all().order_by('-updated_at')
        context = {
            'stocks': stocks,
            'form': form,
            'products': products,
            'cart_items': cart_items
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            print("cost", obj.stock.cost)
            obj.user = request.user
            obj.stock.quantity += form.cleaned_data['quantity']
            obj.cost = form.cleaned_data['cost']
            if obj.cost:
                new_cost = (obj.stock.cost + obj.cost)/2
            else:
                new_cost = obj.stock.cost
            obj.stock.cost = new_cost
            obj.stock.save()
            obj.save()
            return redirect('sales:stock_list')
        context = {
            "form": form
        }
        return render(request, self.template_name, context) 