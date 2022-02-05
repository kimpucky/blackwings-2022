import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related


class User(AbstractUser):
    is_requestor = models.BooleanField('requestor status', default=False)
    is_donor = models.BooleanField('donor status', default=False)
    pass

# class Category(models.Model):
#     category = models.CharField(max_length=64)
#     def __str__(self):
#         return f"{self.category}"

class Listing(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_orders")
    title = models.CharField(max_length=64)
    description = models.TextField()
    initialprice = models.DecimalField(max_digits=16, decimal_places=2)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png")
    sold = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name="bought_orders")
    creationdate = models.DateTimeField(default=datetime.datetime(2021, 9, 29, 1, 50, 16, 283956))
    enddate = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name = "bids")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    biddate = models.DateTimeField()
    def __str__(self):
        return f"Bid on item: {self.listing} by {self.user} at price: ${self.price}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commentdate = models.DateTimeField()
    comment = models.TextField()
    def __str__(self):
        return f"{self.user} wrote: {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)