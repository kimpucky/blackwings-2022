from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms


from .models import *

# categories = Category.objects.all().values_list('category')
# categories = [c[0] for c in categories]


def index(request):
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]

    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(sold=False),
        #"categories" : categories,
        "watchlistIDs" : watchlistIDs
    })

# def category(request, category):
#     category = Category.objects.get(category=category)
#     try:
#         watchlist = Watchlist.objects.filter(user=request.user)
#     except:
#         watchlist = ''
#     watchlistIDs = [l.listing.id for l in watchlist]
#     listings = category.items.all().filter(sold=False)
#     return render(request, "auctions/index.html", {
#         "listings" : listings,
#         #"categories" : categories,
#         #"category" : category,
#         "watchlistIDs" : watchlistIDs
#     })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password.",
                # "categories" : categories,
            })
    else:
        return render(request, "auctions/login.html", {
            # "categories" : categories,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match.",
                # "categories" : categories
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                # "categories" : categories
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html", {
            # "categories" : categories
        })

@login_required
def donate(request):
    donor = request.user
    if request.method == "POST":
        form = DonateForm(request.POST)
        if form.is_valid():
            title = str(form.cleaned_data["title"].title())
            description = str(form.cleaned_data["description"])
            imageurl = str(form.clean_field())
            price = form.cleaned_data["price"]
            # category_id = form.cleaned_data["category"]
            # category = Category.objects.get(pk=category_id)
            creationdate = timezone.localtime()
            listing = Listing(donor=donor, title = title, price = price, description = description, image_url = imageurl, creationdate=creationdate)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            errors = form.errors
            return render(request, "auctions/donate.html", {
                #"categories" : categories,
                "form" : form,
                "error": errors
            })
    else:
        return render(request, "auctions/donate.html", {
            #"categories" : categories,
            #"form": DonateForm(),
            "donor" : donor
        })


@login_required
def watchlist(request, listing_id=''):
    user = request.user
    watchlist = Watchlist.objects.filter(user=user)
    watchlistIDs = [l.listing.id for l in watchlist]
    watchlistview = True

    #if this is just a watchlist view from nav bar with no add or remove
    if listing_id == '':
        listings = [l.listing for l in watchlist]
        return render(request, "auctions/index.html", {
        "watchlistview" : watchlistview,
        "listings" : listings,
        # "categories" : categories,
        "watchlistIDs" : watchlistIDs
        })
    
    print(listing_id)
    listing = Listing.objects.get(id=listing_id)

    #if user clicks on remove from watch list, this is the delete flow
    if listing_id in watchlistIDs:
        delete_listing = Watchlist.objects.get(user=user, listing=listing)
        delete_listing.delete()
        watchlist = Watchlist.objects.filter(user=user)
        listings = [l.listing for l in watchlist]
        return HttpResponseRedirect(reverse("watchlist"))
    #otherwise this is the add flow
    else:
        add_listing = Watchlist(user=user, listing=listing)
        add_listing.save()
        return HttpResponseRedirect(reverse("watchlist"))


def listing(request, listing_id):
    requestor=False
    listing = Listing.objects.get(id=listing_id)
    comments = listing.comments.all().order_by("commentdate")
    form = SoldForm()
    commentform = CommentForm()
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]
    if listing.sold == True:
        if listing.requestor == request.user:
            requestor = True
        else:
            requestor = False

    #if user is not logged in, shows text that user needs to be logged in to bid
    if request.user.is_authenticated == False:
        anonymous = True
        return render(request, "auctions/listing.html", {
                # "categories" : categories,
                "listing" : listing,
                "anonymous" : anonymous,
                "comments" : comments
            })
    #else authenticated users, split into owner of listing and not owner of listing
    else:
        if request.user == listing.donor:
            isOwner = True
        else:
            isOwner = False
        if (request.method == "POST" and 'commentsubmit' in request.POST):
            commentform = CommentForm(request.POST)
            commenttext = str(commentform.data["comment"])
            user = request.user
            newcomment = Comment(user=user, listing=listing, comment=commenttext, commentdate=timezone.localtime())
            newcomment.save()
            commentform = CommentForm()
        
        #if listing is viewed by the owner, show sold checkbox to take listing off the market but no bidding
        if isOwner:
            if (request.method == "POST" and 'soldsubmit' in request.POST):
                form = SoldForm(request.POST)
                soldValue = form.data["sold"]
                if soldValue == 'on':
                    sold = True
                listing.sold = sold
                listing.enddate = timezone.localtime()
               
                listing.save()
                return render(request, "auctions/listing.html", {
                    # "categories" : categories,
                    "listing" : listing,
                    "isOwner": isOwner,
                    "watchlistIDs" : watchlistIDs,
                    "commentform" : commentform,
                    "comments" : comments,
                    "requestor" : requestor
                })
            else:
                return render(request, "auctions/listing.html", {
                    # "categories" : categories,
                    "listing" : listing,
                    "form" : form,
                    "isOwner": isOwner,
                    "watchlistIDs" : watchlistIDs,
                    "commentform" : commentform,
                    "comments" : comments,
                    "requestor" : requestor
                })
        #if listing is viewed by a user who is not the donor, show request options
        else:
            anonymous = False
            return render(request, "auctions/listing.html", {
                # "categories" : categories,
                "listing" : listing,
                "watchlistIDs" : watchlistIDs,
                "commentform" : commentform,
                "comments" : comments,
                "requestor" : requestor
                })




def findPrice(listing_id):
    listing = Listing.objects.get(id=listing_id)
    donorPrice = listing.price
    bids = listing.bids.all().order_by("-biddate")
    #get latest price
    try:
        if (bids[0].price > donorPrice):
            currentPrice = bids[0].price
    except:
        currentPrice = donorPrice
    return currentPrice


class DonateForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea,label="Description")
    imageurl = forms.CharField(widget=forms.URLInput(), label = "Image URL", required=False)
    # category = forms.ChoiceField(widget=forms.Select, choices=Category.objects.all().values_list('id', 'category'), label="Category", )
    price = forms.CharField(widget=forms.NumberInput(), label = "Price")
    def clean_field(self):
        data = self.cleaned_data['imageurl']
        if data == '':
            data = 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png'
        return data
    error_css_class = 'error'
    required_css_class = 'font-weight-bold'    

class SoldForm(forms.Form):
    sold = forms.BooleanField(label="Sold?")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Add Comment")