from django import forms
from sales.models.product import Product
from django.forms import TextInput, Select, FileInput, CheckboxInput, Textarea


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["user", "product_code"]

        widgets = {
            'bar_code': TextInput(attrs={'class': 'form-control', 'id': 'bar_code'}),
            'name': TextInput(attrs={'class': 'form-control', 'id': 'name'}),
            'product_code': TextInput(attrs={'class': 'form-control', 'id': 'product_code'}),
            'model': TextInput(attrs={'class': 'form-control', 'id': 'model'}),
            'description': Textarea(attrs={'class': 'form-control', 'id': 'description'}),
            'cost': TextInput(attrs={'class': 'form-control', 'id': 'cost', 'type': 'number'}),
            'price_margin': TextInput(attrs={'class': 'form-control', 'id': 'price_margin', 'type': 'number'}),
            'price_discount': TextInput(attrs={'class': 'form-control', 'id': 'price_discount', 'type': 'number'}),
            'price': TextInput(attrs={'class': 'form-control', 'id': 'price', 'type': 'number'}),
            'quantity': TextInput(attrs={'class': 'form-control', 'id': 'quantity', 'type': 'number'}),
            'product_warranty': Select(attrs={'class': 'form-control', 'id': 'product_warranty', 'type': 'select'}),
        }