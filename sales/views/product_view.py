from django.shortcuts import render, redirect
from sales.forms.product_form import ProductForm
from sales.models.product import Product
from django.views import View


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
