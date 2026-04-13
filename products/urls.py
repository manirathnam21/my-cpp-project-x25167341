from django.urls import path
from .views import (
    ProductListView,
    # ProductDetailView,  # Comment this out
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    UserProductListView,
    product_detail
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/user/<str:username>/', UserProductListView.as_view(), name='user-products'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Comment this out
    path('products/<int:pk>/', product_detail, name='product-detail'),  # Add this line
    path('products/new/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('category/<int:category_id>/', views.category_products, name='category-products'),
]