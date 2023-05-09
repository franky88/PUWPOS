from django import forms
from sales.models.product import StockTransaction
from django.forms import TextInput, Select, FileInput, CheckboxInput, Textarea

class StockForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = "__all__"
        exclude = ["user"]

        widgets = {
            'stock': Select(attrs={'class': 'form-control', 'id': 'stock'}),
            'quantity': TextInput(attrs={'class': 'form-control', 'id': 'quantity', 'type': 'number', 'name': 'quantity'}),
            'cost': TextInput(attrs={'class': 'form-control', 'id': 'cost', 'type': 'text', 'name': 'cost'}),
        }