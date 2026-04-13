# products/forms.py (create this file if it doesn't exist)
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Form for product reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }