from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from sales.models.order import Customer
from sales.forms.order_form import CustomerForm

class AddCustomerView(View):
    form_class = CustomerForm
    template_name = 'customer/add_customer.html'