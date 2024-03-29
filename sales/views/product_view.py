from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from sales.forms.product_form import ProductForm, ProductCategoryForm, ProductFormat, ProductFormatImport
from sales.forms.stock_form import StockForm
from sales.models.product import Product, StockTransaction, ProductCategory
from sales.addcart import Cart
from django.views import View
from sales.stocktransaction import Stock
from django.views.generic import CreateView
from django.urls import reverse_lazy
import pandas as pd
from tablib import Dataset
from import_export import resources
from sales.admin import ProductResource
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db.models import Sum, Count, F


@method_decorator(login_required, name='dispatch')
class ProductImport(View):
    template_name = 'product_list.html'
    initial = {'key': 'value'}

    def get(self, request):
        format_form = ProductFormatImport(initial=self.initial)
        print(format_form)
        context = {}
        context['format_import_form'] = format_form
        return render(request, self.template_name, context)
    
    def post(self, request):
        file = request.POST.get('file')
        print(file)
        return file

@method_decorator(login_required, name='dispatch')
class ProductImportExport(View):
    template_name = 'product_list.html'
    initial = {'key': 'value'}

    def get(self, request):
        
        format_form = ProductFormat(initial=self.initial)
        context = {
            'format_form': format_form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        qs = Product.objects.all()
        dataset = ProductResource().export(qs)
        format = request.POST.get('format')
        name = request.POST.get('name')
        print(format)
        if format == 'xls':
            ds = dataset.xls
        elif format == 'csv':
            ds = dataset.csv
        else:
            ds = dataset.json
        
        response = HttpResponse(ds, content_type = f'{format}')
        response["Content-Disposition"] = f"attachment; filename={name}.{format}"
        return response
    
@method_decorator(login_required, name='dispatch')
class ProductView(View):
    template_name = 'product_list.html'
    form_class = ProductForm
    category_form_class = ProductCategoryForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        qs = Product.objects.all()
        cart = Cart(request)
        cart_items = cart.__len__()
        format_form = ProductFormat(initial=self.initial)
        form = self.form_class(initial=self.initial)
        category_form = self.category_form_class(initial=self.initial)
        products = qs.order_by('-updated_at', '-created_at')
        categories = ProductCategory.objects.annotate(count=Count('product__id'))
        query = request.GET.get('q')

        if query:
            products = products.filter(
                Q(bar_code__icontains=query) |
                Q(name__icontains=query) |
                Q(model__icontains=query) |
                Q(category__name__icontains=query)
            )

        context = {
            'products': products,
            'form': form,
            'categoryform': category_form,
            'categories': categories,
            'cart_items': cart_items,
            'format_form': format_form
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

@method_decorator(login_required, name='dispatch')
class ProductUpdateView(View):
    template_name = 'product_update.html'
    form_class = ProductForm
    initial = {'key': 'value'}
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        form = self.form_class(request.POST or None, instance=product)
        context = {
            "form": form,
            "instance": product,
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        form = self.form_class(request.POST or None, instance=product)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('sales:product_update', product.id)
        context = {
            "form": form,
            "instance": product,
        }
        return render(request, self.template_name, context)

@login_required()
def importProduct(request):
    product_resource = resources.modelresource_factory(model=Product)()
    dataset = Dataset(['', 'New book'], headers=['id', 'name'])
    result = product_resource.import_data(dataset, dry_run=False)
    return HttpResponse(result)

@login_required()
def exportProduct(request):
    dataset = ProductResource().export()
    print(dataset)
    # return redirect('sales:product_list')
    return HttpResponse(dataset.csv)
# def import_product_data(request):
#     if request.method == 'POST':
#         file = request.FILES['excel']
#         df = pd.read_excel(file)
#         rename_columns = {
#             "bar_code": "bar_code", "name": "name", "model": "model", "description": "description",\
#             "category": "category", "cost": "cost", "price_margin": "price_margin",\
#             "price_discount": "price_discount", "price": "price", "quantity": "quantity",\
#             "is_serial": "is_serial", "product_warranty": "product_warranty"
#             }
#         df.rename(columns = rename_columns, inplace=True)
#         product_resource = ProductResource()
#         dataset = Dataset().load(df)
#         result = product_resource.import_data(dataset, dry_run=True, raise_errors=True)

#         if not result.has_errors():
#             result = product_resource.import_data(dataset, dry_run=False)
#             return redirect("sales:product_list")
        
#     return redirect("sales:product_list")
@login_required()
def add_to_cart(request, id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=id)
    cart.add(product=product, quantity=1, update_quantity=True)
    return redirect('sales:product_list')

@method_decorator(login_required, name='dispatch')
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