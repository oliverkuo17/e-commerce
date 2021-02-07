from django import forms
from django.forms import ModelForm
from .models import *

class CreateListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['item_name', 'description', 'category', 'photo', 'photo_name', 'deadline','starting_bid']

class CreateCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'content']

class CreateBidForm(ModelForm):
    class Meta:
        model = Bid
        fields =  ['amount']
