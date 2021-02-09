from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.seller.id}/{filename}'

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = (
        ("Electronics", "Electronics"),
        ("Motors", "Motors"),
        ("Home & Garden", "Home & Garden" ),
        ("Clothing & Accessories", "Clothing & Accessories"),
        ("Sports", "Sports"),
        ("Health & Beauty", "Health & Beauty"),
        ("Toys", "Toys"),
        ("Business & Industrial", "Business & Industrial"),
        ("Food & Grocery", "Food & Grocery"),
        ("Others", "Others")
    )

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    item_name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='Others')
    photo = models.ImageField(upload_to=user_directory_path)
    photo_name = models.CharField(max_length=64, null=True)
    active = models.BooleanField(default=True)
    deadline = models.DateTimeField()
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2, default=1.00, validators=[MinValueValidator(0.01)])
    current_bid = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, validators=[MinValueValidator((starting_bid))])
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=1024)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(('0.01'))])
