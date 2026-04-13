# admin_panel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin-dashboard'),
    path('users/', views.user_management, name='admin-user-management'),
    path('users/<int:user_id>/', views.user_detail, name='admin-user-detail'),
    path('orders/', views.order_management, name='admin-order-management'),
    path('orders/<int:order_id>/', views.order_detail, name='admin-order-detail'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='admin-update-order-status'),
    path('products/', views.product_management, name='admin-product-management'),
]