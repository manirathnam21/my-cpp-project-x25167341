# admin_panel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import Product, Category, Review
from cart.models import Order, OrderItem

# Check if user is admin
def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard with summary stats"""
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.filter(is_superuser=False).count()
    recent_orders = Order.objects.order_by('-created')[:5]
    
    context = {
        'title': 'Admin Dashboard',
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_orders': recent_orders
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    """Manage users"""
    users = User.objects.filter(is_superuser=False).order_by('-date_joined')
    
    context = {
        'title': 'User Management',
        'users': users
    }
    return render(request, 'admin_panel/user_management.html', context)

@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    """View user details and orders"""
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user).order_by('-created')
    
    context = {
        'title': f'User: {user.username}',
        'user_profile': user,
        'orders': orders
    }
    return render(request, 'admin_panel/user_detail.html', context)

# @login_required
# @user_passes_test(is_admin)
# def order_management(request):
#     """Manage orders"""
#     orders = Order.objects.all().order_by('-created')
    
#     context = {
#         'title': 'Order Management',
#         'orders': orders
#     }
#     return render(request, 'admin_panel/order_management.html', context)


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from cart.models import Order, OrderItem

from orders_csv_export_lib.csv_export import export_queryset_to_csv


@login_required
@user_passes_test(is_admin)
def order_management(request):
    """Manage orders and export to CSV."""
    orders = Order.objects.all().order_by("-created")

    if request.GET.get("export") == "csv":
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created",
        ]
        return export_queryset_to_csv(
            orders,
            fields,
            filename="orders_report.csv",
        )

    context = {
        "title": "Order Management",
        "orders": orders,
    }
    return render(request, "admin_panel/order_management.html", context)

@login_required
@user_passes_test(is_admin)
def order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'title': f'Order #{order.id}',
        'order': order
    }
    return render(request, 'admin_panel/order_detail.html', context)

@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    """Update order status"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('admin-order-detail', order_id=order.id)

@login_required
@user_passes_test(is_admin)
def product_management(request):
    """Manage products"""
    products = Product.objects.all().order_by('-date_posted')
    
    context = {
        'title': 'Product Management',
        'products': products
    }
    return render(request, 'admin_panel/product_management.html', context)