from django.forms import ModelForm
from django.forms import TextInput, NumberInput, EmailInput, Select

from sales.models.order import OrderItem

class SaleForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['products', 'quantity', 'price', 'money_received']

        widgets = {
            'customer': Select(attrs={'class': 'form-control', 'id': 'customer'}),
            # 'money_received': NumberInput(attrs={'class': 'form-control', 'id': 'money_received', 'type': 'number'}),
        }