from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = (
        ("ELE", "Electronics"),
        ("MOT", "Motors"),
        ("HnG", "Home & Garden" ),
        ("CnA", "Clothing & Accessories"),
        ("Spo", "Sports"),
        ("HnB", "Health & Beauty"),
        ("TOY", "Toys"),
        ("BnI", "Business & Industrial"),
        ("FnG", "Food & Grocery"),
        ("OTH", "Others")
    )

    consignor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    item_name = models.CharField(max_length=64)
    description = models.TextField(max_length=2048)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default='OTH')
    photo = models.ImageField(upload_to='%Y/%m/%D/')
    deadline = models.DateTimeField()
    current_price = models.DecimalField(max_digits=9, decimal_places=2, default=1.00)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    title = models.CharField(max_length=64)
    contenct = models.CharField(max_length=1024)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(('0.01'))])

class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlist")
    items = models.ManyToManyField(Listing, blank=True, related_name="watchlist")
