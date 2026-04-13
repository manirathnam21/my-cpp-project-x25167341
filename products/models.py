from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Category model for products"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Product(models.Model):
    """Product model for items"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    materials = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to="product_images",
        default="default_product.jpg",
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pk": self.pk})


class Review(models.Model):
    """Model for product reviews"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name}"