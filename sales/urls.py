from django.urls import path
from sales.views.product_view import ProductView, StockView, add_to_cart
from sales.views.pos_view import POSView, cart_add, cart_updated, cart_remove, cart_clear
from sales.views.order_view import billing_information_view, OrderItemView

app_name = 'sales'
urlpatterns = [
    path('', ProductView.as_view(), name='product_list'),
    path('add-to-cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('sales/', POSView.as_view(), name='pos_view'),
    path('cart/<int:id>/', cart_add, name='cart_add'),
    path('cart-update/<int:id>/', cart_updated, name='cart_updated'),
    path('cart-remove/<int:id>/', cart_remove, name='cart_remove'),
    path('billing-information/', billing_information_view, name='billing_information'),
    path('order-information/', OrderItemView.as_view(), name='order_information'),
    path('stocks/', StockView.as_view(), name="stock_list"),
    path('clear-cart/', cart_clear, name="clear_cart")
]