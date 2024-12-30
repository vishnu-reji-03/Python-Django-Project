from django import forms
from .models import Product,Order,Review

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['name','address','email','phone']

    payment_method = forms.ChoiceField(
        choices=[('cash', 'Cash on Delivery'), ('card', 'Credit/Debit Card')],
        widget=forms.RadioSelect,  # Display as radio buttons
        required=True
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)  # Hidden input to store the star rating value
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}), label='Comment', required=False)