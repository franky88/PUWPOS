from django.urls import path
from sales.views.product_view import ProductView, StockView, add_to_cart, ProductUpdateView, importProduct, exportProduct, ProductImportExport
from sales.views.pos_view import POSView, cart_add, cart_updated, cart_remove, cart_clear
from sales.views.order_view import OrderItemView, customer_order_details, OrderInformationView, OrderListView

app_name = 'sales'
urlpatterns = [
    path('', ProductView.as_view(), name='product_list'),
    path('import-product/', importProduct, name='import_product'),
    path('export-product/', ProductImportExport.as_view(), name='export_product'),
    path('details/<product_id>', ProductUpdateView.as_view(), name='product_update'),
    path('add-to-cart/<int:id>', add_to_cart, name='add_to_cart'),
    path('sales/', POSView.as_view(), name='pos_view'),
    path('cart/<int:id>/', cart_add, name='cart_add'),
    path('cart-update/<int:id>/', cart_updated, name='cart_updated'),
    path('cart-remove/<int:id>/', cart_remove, name='cart_remove'),
    path('billing-information/', OrderInformationView.as_view(), name='billing_information'),
    path('order-information/', OrderItemView.as_view(), name='order_information'),
    path('stocks/', StockView.as_view(), name="stock_list"),
    path('orders/', OrderListView.as_view(), name="order_list_view"),
    path('clear-cart/', cart_clear, name="clear_cart"),
    path('customer-order-details/<int:pk>', customer_order_details, name="customer_orders")
]