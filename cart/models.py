# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class CartItem(models.Model):
    """Model for storing items in a user's shopping cart"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.product.price * self.quantity

class Order(models.Model):
    """Model for tracking orders"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    """Model for storing individual items within an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    def get_total_price(self):
        return self.price * self.quantity