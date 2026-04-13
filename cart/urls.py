# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy-now'),
    path('', views.view_cart, name='cart'),
    path('update/<int:item_id>/', views.update_cart, name='update-cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order-confirmation'),
    path('order-history/', views.order_history, name='order-history'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel-order'),
]