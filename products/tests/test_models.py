# products/tests/test_models.py
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category, Product, Review

@pytest.fixture
def category(db):
    """Create a test category"""
    return Category.objects.create(
        name='Test Category',
        description='Test Category Description'
    )

@pytest.fixture
def user(db):
    """Create a test user"""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword'
    )
    return user

@pytest.fixture
def product(db, category, user):
    """Create a test product"""
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
def review(db, product, user):
    """Create a test review"""
    return Review.objects.create(
        product=product,
        user=user,
        rating=4,
        comment="This is a test review"
    )

@pytest.mark.django_db
def test_product_creation(product):
    """Test that a product can be created and saved to the database"""
    assert Product.objects.count() == 1
    assert Product.objects.get(id=product.id).name == 'Test Product'

@pytest.mark.django_db
def test_product_str_method(product):
    """Test the __str__ method of the Product model"""
    assert str(product) == 'Test Product'

@pytest.mark.django_db
def test_category_str_method(category):
    """Test the __str__ method of the Category model"""
    assert str(category) == 'Test Category'

@pytest.mark.django_db
def test_product_get_absolute_url(product):
    """Test the get_absolute_url method of the Product model"""
    url = product.get_absolute_url()
    assert url == reverse('product-detail', kwargs={'pk': product.pk})

@pytest.mark.django_db
def test_review_creation(review):
    """Test that a review can be created and saved to the database"""
    assert Review.objects.count() == 1
    assert Review.objects.get(id=review.id).rating == 4

@pytest.mark.django_db
def test_review_str_method(review, user, product):
    """Test the __str__ method of the Review model"""
    expected = f"{user.username}'s review for {product.name}"
    assert str(review) == expected