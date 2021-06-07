from django.contrib.auth.models import AbstractUser
from django.db import models
from commerce.settings import AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

CATEGORY = (
    ("BOOKS", "Books"),
    ("ELECTRONICS", "Electronics"),
    ("FASHIONS", "Fashions"),
    ("HOME", "Home"),
    ("GAMES", "Games & Toys")
)


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listing_user")
    description = models.TextField()
    image = models.URLField()
    start_bid = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999999999)])
    category = models.CharField(max_length=20, choices=CATEGORY)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    body = models.TextField()

    def __str__(self):
        return f"{self.user}'s comment on {self.listing}"


class Bid(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bid = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999999999)])

    def __str__(self):
        return f"{self.user}'s bid on {self.listing}"


class Watchlist(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.user}'s watchlist"
