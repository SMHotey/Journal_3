from django.urls import path
from .views import order_view, orders_list, delete_order
import re

urlpatterns = [
    path('upload/', order_view, name='upload_view'),
    path('orders/', orders_list, name='orders_list'),
    path('delete/<int:order_id>/', delete_order, name='delete_order'),
]