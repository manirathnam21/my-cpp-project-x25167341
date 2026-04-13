from django import template
from products.models import Review

register = template.Library()

@register.filter
def has_reviewed(user, product):
    """Check if the user has reviewed the product"""
    if not user.is_authenticated:
        return False
    return Review.objects.filter(user=user, product=product).exists()