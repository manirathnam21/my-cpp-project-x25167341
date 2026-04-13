# cart/tests/test_cart.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product
from cart.models import CartItem, Order, OrderItem

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword'
    )

@pytest.fixture
def category(db):
    return Category.objects.create(
        name='Test Category',
        description='Test Category Description'
    )

@pytest.fixture
def product(db, category, user):
    return Product.objects.create(
        name='Test Product',
        description='Test Product Description',
        price=99.99,
        category=category,
        sustainability_score=75,
        materials='Organic Cotton',
        seller=user,
        in_stock=True
    )

@pytest.fixture
def cart_item(db, user, product):
    return CartItem.objects.create(
        user=user,
        product=product,
        quantity=2
    )

@pytest.fixture
def order(db, user):
    return Order.objects.create(
        user=user,
        full_name="Test User",
        email="test@example.com",
        address="123 Test St",
        city="Test City",
        postal_code="12345",
        country="Test Country",
        total_price=199.98
    )

@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        price=99.99,
        quantity=2
    )

@pytest.mark.django_db
def test_cart_item_creation(cart_item):
    """Test that a cart item can be created"""
    assert CartItem.objects.count() == 1
    assert cart_item.quantity == 2

@pytest.mark.django_db
def test_cart_item_total_price(cart_item, product):
    """Test the get_total_price method of CartItem"""
    assert cart_item.get_total_price() == product.price * cart_item.quantity

@pytest.mark.django_db
def test_order_creation(order):
    """Test that an order can be created"""
    assert Order.objects.count() == 1
    assert order.full_name == "Test User"

@pytest.mark.django_db
def test_order_item_creation(order_item):
    """Test that an order item can be created"""
    assert OrderItem.objects.count() == 1
    assert order_item.quantity == 2

@pytest.mark.django_db
def test_order_item_total_price(order_item):
    """Test the get_total_price method of OrderItem"""
    assert order_item.get_total_price() == order_item.price * order_item.quantity

@pytest.mark.django_db
def test_view_cart_authenticated(client, user):
    """Test that authenticated users can view their cart"""
    client.force_login(user)
    response = client.get(reverse('cart'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_view_cart_unauthenticated(client):
    """Test that unauthenticated users are redirected when trying to view cart"""
    response = client.get(reverse('cart'))
    assert response.status_code == 302  # Redirect to login