from django.forms import ModelForm
from django.forms import TextInput, NumberInput, EmailInput, Select

from sales.models.order import OrderItem

class SaleForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['order_id','products', 'quantity', 'price',]

        widgets = {
            'customer': Select(attrs={'class': 'form-control', 'id': 'customer'}),
            'money_tender': NumberInput(attrs={'class': 'form-control', 'id': 'money_tender', 'type': 'number'}),
        }