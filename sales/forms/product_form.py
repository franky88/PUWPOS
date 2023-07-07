from django import forms
from sales.models.product import Product, ProductCategory
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
            'cost': TextInput(attrs={'class': 'form-control', 'id': 'cost', 'type': 'text'}),
            'category': Select(attrs={'class': 'form-control', 'id': 'category', 'type': 'select'}),
            'price_margin': TextInput(attrs={'class': 'form-control', 'id': 'price_margin', 'type': 'text'}),
            'price_discount': TextInput(attrs={'class': 'form-control', 'id': 'price_discount', 'type': 'text'}),
            'price': TextInput(attrs={'class': 'form-control', 'id': 'price', 'type': 'text'}),
            'quantity': TextInput(attrs={'class': 'form-control', 'id': 'quantity', 'type': 'number'}),
            'product_warranty': Select(attrs={'class': 'form-control', 'id': 'product_warranty', 'type': 'select'}),
            'image': Select(attrs={'class': 'form-control', 'id': 'image', 'type': 'select'}),
        }

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = "__all__"

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'id': 'category-name'})
        }

FORMAT_CHOICES = (
    ('xls', 'xls'),
    ('csv', 'csv'),
    ('json', 'json'),
)

class ProductFormat(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    format = forms.ChoiceField(choices=FORMAT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

class ProductFormatImport(forms.Form):
    file = forms.FileField(widget=FileInput(attrs={"class": "form-control"}))
    name = forms.CharField(widget=TextInput(attrs={"class": "form-control"}))
    # file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))