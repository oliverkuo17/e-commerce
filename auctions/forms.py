from django import forms
from django.forms import ModelForm
from .models import *

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'description', 'category', 'photo', 'photo_name', 'deadline','starting_bid']
        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'photo_name': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control'})
        }

class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']

class CreateBidForm(ModelForm):
    class Meta:
        model = Bid
        fields =  ['amount']
