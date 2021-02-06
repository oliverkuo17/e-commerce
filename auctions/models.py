from django.contrib.auth.models import AbstractUser
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
    item_name = models.CharField(max_length=64)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default = 'OTH')
    deadline = models.DateTimeField()