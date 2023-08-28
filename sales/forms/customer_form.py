from django.forms import ModelForm
from django.forms import TextInput, NumberInput, EmailInput

from sales.models.order import Customer


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter Full Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter email address'}),
            'number': NumberInput(attrs={'class': 'form-control', 'id': 'number'}),
            'address': TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Enter address'})
        }