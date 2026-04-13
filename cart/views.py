# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from django.http import HttpResponseRedirect
from django.urls import reverse
from products.models import Product
from .models import CartItem, Order, OrderItem
from .forms import AddToCartForm, OrderForm
from decimal import Decimal

@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Check if product is in stock
            if not product.in_stock:
                messages.error(request, "Sorry, this product is out of stock.")
                return HttpResponseRedirect(reverse('product-detail', args=[product_id]))
            
            # Check if item already in cart
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            # Update quantity if item already exists
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
                messages.success(request, f"Updated {product.name} quantity in your cart.")
            else:
                messages.success(request, f"Added {product.name} to your cart.")
            
            return redirect('cart')
    else:
        return redirect('product-detail', pk=product_id)

@login_required
def view_cart(request):
    """View the user's current shopping cart"""
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'title': 'Shopping Cart'
    }
    return render(request, 'cart/cart.html', context)

@login_required
def update_cart(request, item_id):
    """Update the quantity of an item in the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item.quantity = form.cleaned_data['quantity']
            cart_item.save()
            messages.success(request, f"Updated {cart_item.product.name} quantity.")
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Removed {product_name} from your cart.")
    return redirect('cart')

@login_required
def checkout(request):
    """Process the checkout and create an order"""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty. Please add items before checkout.")
        return redirect('products')
    
    total = sum(item.get_total_price() for item in cart_items)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total
            order.save()
            
            # Create order items from cart items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
            
            # Clear the cart
            cart_items.delete()
            
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order-confirmation', order_id=order.id)
    else:
        # Pre-fill form with user info if available
        initial_data = {}
        if hasattr(request.user, 'email'):
            initial_data['email'] = request.user.email
        if hasattr(request.user, 'get_full_name'):
            initial_data['full_name'] = request.user.get_full_name()
            
        form = OrderForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'total': total,
        'title': 'Checkout'
    }
    return render(request, 'cart/checkout.html', context)



import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
def order_confirmation(request, order_id):
    """Display order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'title': 'Order Confirmation'
    }

    return render(request, 'cart/order_confirmation.html', context)


    

@login_required
def buy_now(request, product_id):
    """Implement buy now functionality (add to cart and go to checkout)"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            # Check if product is in stock
            if not product.in_stock:
                messages.error(request, "Sorry, this product is out of stock.")
                return HttpResponseRedirect(reverse('product-detail', args=[product_id]))
            
            # Remove any existing cart items for this product
            CartItem.objects.filter(user=request.user, product=product).delete()
            
            # Add new cart item with specified quantity
            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=quantity
            )
            
            messages.success(request, f"Added {product.name} to your cart. Proceeding to checkout.")
            return redirect('checkout')
    else:
        return redirect('product-detail', pk=product_id)

@login_required
def order_history(request):
    """View order history"""
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    context = {
        'orders': orders,
        'title': 'Order History'
    }
    return render(request, 'cart/order_history.html', context)

@login_required
def order_detail(request, order_id):
    """View details of a specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'title': f'Order #{order.id}'
    }
    return render(request, 'cart/order_detail.html', context)

@login_required
def cancel_order(request, order_id):
    """Cancel an order if it's in pending status"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} has been successfully cancelled.')
    else:
        messages.error(request, f'Order #{order.id} cannot be cancelled as it is already {order.get_status_display()}.')
    
    return redirect('order-detail', order_id=order.id)