from django.shortcuts import render, redirect, get_object_or_404
from sales.forms.product_form import ProductForm
from sales.forms.stock_form import StockForm
from sales.models.product import Product, StockTransaction
from django.views import View
from sales.stocktransaction import Stock
from django.views.generic import CreateView
from django.urls import reverse_lazy


class ProductView(View):
    template_name = 'product_list.html'
    form_class = ProductForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        products = Product.objects.all().order_by('-updated_at', '-created_at')
        context = {
            'products': products,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('sales:product_list')
        context = {
            "form": form
        }
        return render(request, self.template_name, context)
    
class StockView(View):
    template_name = 'stock/stock_list.html'
    form_class = StockForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        stocks = StockTransaction.objects.all().order_by('-timestamp')
        context = {
            'stocks': stocks,
            'form': form,
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