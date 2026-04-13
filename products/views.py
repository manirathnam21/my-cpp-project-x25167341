from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from django.db.models import Avg
from .models import Review
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Product, Category
import boto3


# This function checks if user is admin
def is_admin(user):
    return user.is_superuser

def home(request):
    """Home page view with featured products"""
    context = {
        'products': Product.objects.all()[:6],  # Show only 6 products on home page
        'categories': Category.objects.all(),
        'title': 'Home'
    }
    return render(request, 'products/home.html', context)

class ProductListView(ListView):
    """View all products with pagination"""
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    ordering = ['-date_posted']
    paginate_by = 8
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Products'
        context['categories'] = Category.objects.all()
        return context

class UserProductListView(ListView):
    model = Product
    template_name = 'products/user_products.html'
    context_object_name = 'products'
    paginate_by = 8
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Product.objects.filter(seller=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        context['title'] = f"{username}'s Products"
        context['seller'] = user
        return context

# class ProductDetailView(DetailView):
    """View product details"""
    model = Product
    template_name = 'products/product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

# def product_detail(request, pk):
#     """View product details with reviews"""
#     product = get_object_or_404(Product, id=pk)
#     reviews = product.reviews.all()
    
#     # Initialize variables
#     review_form = None
#     has_reviewed = False
    
#     if request.user.is_authenticated:
#         # Check if user already reviewed this product
#         has_reviewed = Review.objects.filter(product=product, user=request.user).exists()
        
#         # Form handling
#         if request.method == 'POST':
#             review_form = ReviewForm(request.POST)
#             if review_form.is_valid():
#                 existing_review = Review.objects.filter(product=product, user=request.user).first()
                
#                 if existing_review:
#                     # Update existing review
#                     existing_review.rating = review_form.cleaned_data['rating']
#                     existing_review.comment = review_form.cleaned_data['comment']
#                     existing_review.save()
#                     messages.success(request, "Your review has been updated!")
#                 else:
#                     # Create new review
#                     new_review = review_form.save(commit=False)
#                     new_review.product = product
#                     new_review.user = request.user
#                     new_review.save()
#                     messages.success(request, "Your review has been added!")
                    
#                 return redirect('product-detail', pk=pk)
#         else:
#             # Pre-populate form if user has already reviewed
#             existing_review = Review.objects.filter(product=product, user=request.user).first()
#             if existing_review:
#                 review_form = ReviewForm(instance=existing_review)
#             else:
#                 review_form = ReviewForm()
#     else:
#         review_form = ReviewForm()
    
#     # Calculate average rating
#     avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
#     print(f"Average Rating: {avg_rating}")
    

#     context = {
#         'product': product,
#         'reviews': reviews,
#         'review_form': review_form,
#         'avg_rating': avg_rating,
#         'has_reviewed': has_reviewed,  # Add this variable
#         'title': product.name
#     }
#     return render(request, 'products/product_detail.html', context)






# import requests
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from django.db.models import Avg
# from .models import Product, Review
# from .forms import ReviewForm


# API_URL = "https://9hpuwivakg.execute-api.us-east-1.amazonaws.com/default/lambda-cpp-x25167341"


# def product_detail(request, pk):
#     """View product details with reviews"""
#     product = get_object_or_404(Product, id=pk)
#     reviews = product.reviews.all()

#     review_form = None
#     has_reviewed = False

#     if request.user.is_authenticated:
#         has_reviewed = Review.objects.filter(
#             product=product,
#             user=request.user
#         ).exists()

#         if request.method == "POST":
#             review_form = ReviewForm(request.POST)

#             if review_form.is_valid():
#                 existing_review = Review.objects.filter(
#                     product=product,
#                     user=request.user
#                 ).first()

#                 if existing_review:
#                     existing_review.rating = review_form.cleaned_data["rating"]
#                     existing_review.comment = review_form.cleaned_data["comment"]
#                     existing_review.save()
#                     messages.success(request, "Your review has been updated!")
#                 else:
#                     new_review = review_form.save(commit=False)
#                     new_review.product = product
#                     new_review.user = request.user
#                     new_review.save()
#                     messages.success(request, "Your review has been added!")

#                 return redirect("product-detail", pk=pk)

#         else:
#             existing_review = Review.objects.filter(
#                 product=product,
#                 user=request.user
#             ).first()

#             if existing_review:
#                 review_form = ReviewForm(instance=existing_review)
#             else:
#                 review_form = ReviewForm()
#     else:
#         review_form = ReviewForm()

#     # Prepare review data for Lambda
#     review_data = [{"rating": review.rating} for review in reviews]

#     avg_rating = 0

#     try:
#         response = requests.post(
#             API_URL,
#             json={"reviews": review_data},
#             timeout=5
#         )

#         if response.status_code == 200:
#             result = response.json()

#             # Some API Gateway responses wrap the body
#             if "body" in result:
#                 body = result["body"]
#                 if isinstance(body, str):
#                     import json
#                     body = json.loads(body)
#                 avg_rating = body.get("average_rating", 0)
#             else:
#                 avg_rating = result.get("average_rating", 0)

#     except Exception as e:
#         print("Lambda API error:", e)
#         # fallback to local calculation
#         avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

#     context = {
#         "product": product,
#         "reviews": reviews,
#         "review_form": review_form,
#         "avg_rating": avg_rating,
#         "has_reviewed": has_reviewed,
#         "title": product.name,
#     }

#     return render(request, "products/product_detail.html", context)



import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg
from .models import Product, Review
from .forms import ReviewForm

API_URL = "https://9hpuwivakg.execute-api.us-east-1.amazonaws.com/default/lambda-cpp-x25167341"


def product_detail(request, pk):
    """View product details with reviews"""
    product = get_object_or_404(Product, id=pk)
    reviews = product.reviews.all()

    review_form = None
    has_reviewed = False

    # Check authentication
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(
            product=product,
            user=request.user
        ).exists()

        if request.method == "POST":
            review_form = ReviewForm(request.POST)

            if review_form.is_valid():
                existing_review = Review.objects.filter(
                    product=product,
                    user=request.user
                ).first()

                if existing_review:
                    existing_review.rating = review_form.cleaned_data["rating"]
                    existing_review.comment = review_form.cleaned_data["comment"]
                    existing_review.save()
                    messages.success(request, "Your review has been updated!")
                else:
                    new_review = review_form.save(commit=False)
                    new_review.product = product
                    new_review.user = request.user
                    new_review.save()
                    messages.success(request, "Your review has been added!")

                return redirect("product-detail", pk=pk)

        else:
            existing_review = Review.objects.filter(
                product=product,
                user=request.user
            ).first()

            if existing_review:
                review_form = ReviewForm(instance=existing_review)
            else:
                review_form = ReviewForm()
    else:
        review_form = ReviewForm()

    # Send review ratings to Lambda
    review_data = [{"rating": review.rating} for review in reviews]

    avg_rating = 0

    try:
        response = requests.post(
            API_URL,
            json={"reviews": review_data},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()

            # API Gateway wraps Lambda response inside "body"
            if isinstance(data, dict) and "body" in data:
                body = data["body"]

                if isinstance(body, str):
                    body = json.loads(body)

                avg_rating = float(body.get("average_rating", 0))
            else:
                avg_rating = float(data.get("average_rating", 0))

    except Exception as e:
        print("Lambda API error:", e)

        # Fallback to Django calculation
        avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    avg_rating = float(avg_rating or 0)

    context = {
        "product": product,
        "reviews": reviews,
        "review_form": review_form,
        "avg_rating": avg_rating,
        "has_reviewed": has_reviewed,
        "title": product.name,
    }

    return render(request, "products/product_detail.html", context)









class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Create new product (admin only)"""
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'category', 'materials', 'image', 'in_stock']

    
    """ def form_valid(self, form):
        form.instance.seller = self.request.user

        if self.object.image:
            local_path = self.object.image.path
            image_upload_s3(local_path, f'products/{self.object.image.name}')
        return super().form_valid(form) """
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)

        if self.object.image:
            try:
                image_upload_s3(self.object.image.path, self.object.image.name)
                print(" Calling sns_email now...")
                sns_email(
                    self.object.name,
                    self.object.description,
                    self.object.price,
                    self.object.category.name,
                    self.object.materials,
                    self.object.image.url,
                    self.object.in_stock
                )
            except Exception as e:
                print(f" S3 upload or SNS email failed: {e}")

        return response


    def test_func(self):
        return is_admin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Product'
        context['button_text'] = 'Add Product'
        return context

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing product (admin only)"""
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description', 'price', 'category', 'materials', 'image', 'in_stock']
    
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Product'
        context['button_text'] = 'Update Product'
        return context

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete product (admin only)"""
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        return is_admin(self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Product'
        return context

def category_products(request, category_id):
    """View products by category"""
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category).order_by('-date_posted')
    context = {
        'category': category,
        'products': products,
        'title': f'{category.name} Products'
    }
    return render(request, 'products/category_products.html', context)


def image_upload_s3(file_path, object_name=None):
        bucket_name = "s3-cpp-x25167341" 
        if object_name is None:
            object_name = file_path.split('/')[-1]
        s3_client = boto3.client('s3', region_name="us-east-1")
        try:
            with open(file_path, "rb") as file_data:
                s3_client.upload_fileobj(file_data, bucket_name, object_name)
            print(f"Successfully uploaded {object_name} to {bucket_name}")
            return True
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
            return False


def sns_email(name, description, price, category, materials, image_url, in_stock):
    
    full_message = f""" New Product Added: {name}
    Description: {description}
    Price: ${price}
    Category: {category}    
    Materials: {materials}
    Image URL: {image_url}
    In Stock: {'Yes' if in_stock else 'No'}
    Please check the admin panel for more details.
    """

    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:877651420591:sns-cpp-x25167341"

    try:
        sns_client = boto3.client("sns", region_name="us-east-1")  
        
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=full_message,
            Subject="New Product Added to Store",
        )
        
        print(f"Email sent successfully! Message ID: {response['MessageId']}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False
