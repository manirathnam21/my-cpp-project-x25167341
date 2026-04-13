# products/tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product, Review

@pytest.fixture
def category(db):
    return Category.objects.create(
        name='Test Category',
        description='Test Category Description'
    )

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword'
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )

@pytest.fixture
def product(db, category, admin_user):
    return Product.objects.create(
        name='Test Product',
        description='Test Product Description',
        price=99.99,
        category=category,
        sustainability_score=75,
        materials='Organic Cotton',
        seller=admin_user,
        in_stock=True
    )

@pytest.mark.django_db
def test_home_view(client):
    """Test that the home view returns a 200 status code"""
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert ' Marketplace' in str(response.content)

@pytest.mark.django_db
def test_product_list_view(client, product):
    """Test that the product list view returns a 200 status code and contains the product"""
    response = client.get(reverse('products'))
    assert response.status_code == 200
    assert product.name in str(response.content)

@pytest.mark.django_db
def test_product_detail_view(client, product):
    """Test that the product detail view returns a 200 status code and contains the product details"""
    response = client.get(reverse('product-detail', kwargs={'pk': product.pk}))
    assert response.status_code == 200
    assert product.name in str(response.content)
    assert product.description in str(response.content)
    assert str(product.price) in str(response.content)

@pytest.mark.django_db
def test_product_create_view_regular_user(client, user):
    """Test that regular users cannot access product create view"""
    client.force_login(user)
    response = client.get(reverse('product-create'))
    assert response.status_code == 403  # Forbidden

@pytest.mark.django_db
def test_product_create_view_admin(client, admin_user):
    """Test that admin users can access product create view"""
    client.force_login(admin_user)
    response = client.get(reverse('product-create'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_update_view_admin(client, admin_user, product):
    """Test that admin users can access product update view"""
    client.force_login(admin_user)
    response = client.get(reverse('product-update', kwargs={'pk': product.pk}))
    assert response.status_code == 200

@pytest.mark.django_db
def test_category_products_view(client, category, product):
    """Test the category products view"""
    response = client.get(reverse('category-products', kwargs={'category_id': category.id}))
    assert response.status_code == 200
    assert product.name in str(response.content)