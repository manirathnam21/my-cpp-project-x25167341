# import pytest
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Category, Product

# @pytest.fixture
# def category(db):
#     """Create a test category"""
#     return Category.objects.create(
#         name='Test Category',
#         description='Test Category Description'
#     )

# @pytest.fixture
# def user(db):
#     """Create a test user"""
#     user = User.objects.create_user(
#         username='testuser',
#         email='test@example.com',
#         password='testpassword'
#     )
#     return user

# @pytest.fixture
# def product(db, category, user):
#     """Create a test product"""
#     return Product.objects.create(
#         name='Test Product',
#         description='Test Product Description',
#         price=99.99,
#         category=category,
#         sustainability_score=75,
#         materials='Organic Cotton',
#         seller=user,
#         in_stock=True
#     )

# @pytest.mark.django_db
# def test_product_creation(product):
#     """Test that a product can be created and saved to the database"""
#     assert Product.objects.count() == 1
#     assert Product.objects.get(id=product.id).name == 'Test Product'

# @pytest.mark.django_db
# def test_product_str_method(product):
#     """Test the __str__ method of the Product model"""
#     assert str(product) == 'Test Product'

# @pytest.mark.django_db
# def test_category_str_method(category):
#     """Test the __str__ method of the Category model"""
#     assert str(category) == 'Test Category'

# @pytest.mark.django_db
# def test_product_get_absolute_url(product):
#     """Test the get_absolute_url method of the Product model"""
#     url = product.get_absolute_url()
#     assert url == reverse('product-detail', kwargs={'pk': product.pk})

# @pytest.mark.django_db
# def test_home_view(client):
#     """Test that the home view returns a 200 status code"""
#     response = client.get(reverse('home'))
#     assert response.status_code == 200
#     assert ' Marketplace' in str(response.content)

# @pytest.mark.django_db
# def test_product_list_view(client, product):
#     """Test that the product list view returns a 200 status code and contains the product"""
#     response = client.get(reverse('products'))
#     assert response.status_code == 200
#     assert product.name in str(response.content)

# @pytest.mark.django_db
# def test_product_detail_view(client, product):
#     """Test that the product detail view returns a 200 status code and contains the product details"""
#     response = client.get(reverse('product-detail', kwargs={'pk': product.pk}))
#     assert response.status_code == 200
#     assert product.name in str(response.content)
#     assert product.description in str(response.content)
#     assert str(product.price) in str(response.content)