import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User





class Profile(models.Model):
    username = models.CharField("username", max_length = 512, blank = True,null=True)
    is_requestor = models.BooleanField('Requestor Status', default=False,null=True)
    is_donor = models.BooleanField('Donor Status', default=True,null=True)
    #image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    confirmed = models.BooleanField("Confirmed", default=False,null=True)

    firstname = models.CharField("First Name", max_length = 512, blank = True,null=True)
    lastname = models.CharField("Last Name", max_length = 512, blank = True,null=True)
    school = models.CharField("School", max_length = 512, blank = True,null=True)
    address1= models.CharField("Address Line 1", max_length = 512, blank = True,null=True)
    address2= models.CharField("Address Line 2", max_length = 512, blank = True,null=True)
    city = models.CharField("City", max_length=50, blank=True,null=True)
    state = models.CharField("State", max_length=50, blank=True,null=True)
    zipcode = models.DecimalField("Zip Code", max_digits=5,decimal_places=0, blank = True, null=True)
    def __str__(self):
        return f"{self.username}"

class User(AbstractUser):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True)

class Category(models.Model):
     category = models.CharField(max_length=64,default="Other")
     def __str__(self):
         return f"{self.category}"

class Listing(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    initialprice = models.DecimalField(max_digits=16, decimal_places=2,default=0)
    image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png")
    sold = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name="bought_orders")
    creationdate = models.DateTimeField(default=datetime.datetime(2021, 9, 29, 1, 50, 16, 283956))
    enddate = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return f"{self.title}"

class Requesting(models.Model):
    requestor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    title = models.CharField(max_length=64)
    description = models.TextField()
    requestorcategory = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="request_items")
    image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png")
    sold = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=16, decimal_places=2,default=0)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null= True, related_name="request_donor")
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