from xml.dom.minidom import Identified
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.messages import constants as messages



from .models import *


def get_categories():
    categories = Category.objects.all().values_list('category')
    categories = [c[0] for c in categories]
    return categories

def get_request_categories():
    requestorcategories = RequestorCategory.objects.all().values_list('category')
    requestorcategories = [c[0] for c in requestorcategories]
    return requestorcategories

def indexlisting(request):
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]

    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(sold=False),
        "categories" : get_categories(),
        "requestorcategory": get_request_categories(),
        "watchlistIDs" : watchlistIDs
    })

def indexrequesting(request):
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]

    return render(request, "auctions/indexrequesting.html", {
        "listings" : Listing.objects.filter(sold=False),
        "requestings" : Requesting.objects.filter(sold=False),
        "categories" : get_categories(),
        "requestorcategory": get_request_categories(),
        "watchlistIDs" : watchlistIDs
    })


def category(request, category):
    category = Category.objects.get(category=category)
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]
    listings = category.items.all().filter(sold=False)
    return render(request, "auctions/indexlisting.html", {
        "listings" : listings,
        "categories" : get_categories(),
        "requestorcategory" : get_request_categories(),
        "category" : category,
        "watchlistIDs" : watchlistIDs
    })

def requestorcategory(request, category):
    category = RequestorCategory.objects.get(category=category)
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]
    requestings = category.request_items.all().filter(sold=False)
    return render(request, "auctions/indexrequesting.html", {
        "requestings" : requestings,
        "requestorcategories" : get_request_categories(),
        "categories" : get_categories(),
        "category" : category,
        "watchlistIDs" : watchlistIDs
    })
    

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
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
            })
    else:
        return render(request, "auctions/login.html", {
            "categories" : get_categories(),
            "requestorcategory" : get_request_categories(),

        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def profile(request):
    user = request.user
    if user.profile == None:
        if request.method == 'POST':
            p_reg_form = ProfileRegisterForm(request.POST)
            if p_reg_form.is_valid():
                firstname=p_reg_form.data['firstname']
                lastname=p_reg_form.data['lastname']
                school=p_reg_form.data['school']
                address1=p_reg_form.data['address1']
                address2=p_reg_form.data['address2']
                city=p_reg_form.data['city']
                state=p_reg_form.data['state']
                zipcode=p_reg_form.data['zipcode']
                is_donor= p_reg_form.cleaned_data['is_donor']
                is_requestor= p_reg_form.cleaned_data['is_requestor']
                profile=Profile(username = user.username,firstname=firstname, lastname=lastname, school=school,address1=address1,address2=address2,city=city, state=state,zipcode=zipcode,is_donor=is_donor, is_requestor=is_requestor)
                profile.save()
                user.profile = profile
                user.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            p_reg_form = ProfileRegisterForm()
        context = {
        'p_reg_form': p_reg_form}
        return render(request, 'auctions/profile.html', context)
    else:
        u = user.profile
        p_reg_form = ProfileRegisterForm(instance=u)
        context = {
            'p_reg_form': p_reg_form}
        return render(request, 'auctions/profile.html', context)


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
                "categories" : get_categories()
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken.",
                "categories" : get_categories()
            })
        login(request, user)
        return HttpResponseRedirect('profile')
    else:
        return render(request, "auctions/register.html", {
            "categories" : get_categories()
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
            category_id = form.cleaned_data["category"]
            id = int(category_id)
            category = Category.objects.get(pk=id)
            creationdate = timezone.localtime()
            listing = Listing(
                donor=donor,
                title = title,
                price = price,
                description = description,
                category=category,
                image_url = imageurl,
                creationdate=creationdate)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            errors = form.errors
            return render(request, "auctions/donate.html", {
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
                "form" : form,
                "error": errors
            })
    else:
        return render(request, "auctions/donate.html", {
            "categories" : get_categories(),
            "requestorcategory" : get_request_categories(),
            "form": DonateForm(),
            "donor" : donor
        })

@login_required
def askfordonation(request):
    requestor = request.user
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            title = str(form.cleaned_data["title"].title())
            description = str(form.cleaned_data["description"])
            imageurl = str(form.clean_field())
            requestorcategory_id = form.cleaned_data["requestorcategory"]
            id = int(requestorcategory_id)
            requestorcategory = RequestorCategory.objects.get(pk=id)
            creationdate = timezone.localtime()
            requestlisting = Requesting(
                requestor=requestor,
                title = title,
                description = description,
                requestorcategory=requestorcategory,
                image_url = imageurl,
                creationdate=creationdate)
            requestlisting.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            errors = form.errors
            return render(request, "auctions/askfordonation.html", {
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
                "form" : form,
                "error": errors
            })
    else:
        return render(request, "auctions/askfordonation.html", {
            "categories" : get_categories(),
            "requestorcategory" : get_request_categories(),
            "form": RequestForm(),
            "requestor" : requestor
        })

def add_to_watchlist(request, listing_id):
    add_listing = Watchlist(user=request.user, listing_id=listing_id)
    add_listing.save()

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
        "categories" : get_categories(),
        "requestorcategory" : get_request_categories(),
        "watchlistIDs" : watchlistIDs
        })
    

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
    matchform = RequestorMatch()

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
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
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

        if request.user.profile.is_requestor == True:
            is_requestor = True
        else:
            is_requestor = False
        
        if (request.method == "POST" and 'commentsubmit' in request.POST):
            commentform = CommentForm(request.POST)
            commenttext = str(commentform.data["comment"])
            user = request.user
            newcomment = Comment(user=user, listing=listing, comment=commenttext, commentdate=timezone.localtime())
            newcomment.save()
            commentform = CommentForm()
        
        #if listing is viewed by the owner, show sold checkbox to take listing off the market
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
                    "categories" : get_categories(),
                    "requestorcategory" : get_request_categories(),
                    "listing" : listing,
                    "isOwner": isOwner,
                    "watchlistIDs" : watchlistIDs,
                    "commentform" : commentform,
                    "comments" : comments,
                    "requestor" : requestor
                })
            else:
                return render(request, "auctions/listing.html", {
                    "categories" : get_categories(),
                    "requestorcategory" : get_request_categories(),
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
            if is_requestor:
                matchform = RequestorMatch()
                if (request.method == "POST" and 'matchsubmit' in request.POST):
                    matchform = RequestorMatch(request.POST)
                    matchValue = matchform.data["match"]
                    if matchValue == 'on':
                        match = True
                    listing.sold = True
                    listing.requestor = request.user
                    listing.enddate = timezone.localtime() 
                    listing.save()
                    return render(request, "auctions/listing.html", {
                        "categories" : get_categories(),
                        "requestorcategory" : get_request_categories(),
                        "listing" : listing,
                        "watchlistIDs" : watchlistIDs,
                        "matchform" : matchform,
                        "is_requestor": is_requestor,
                        "commentform" : commentform,
                        "comments" : comments,
                        "requestor" : requestor
                    })
                return render(request, "auctions/listing.html", {
                        "categories" : get_categories(),
                        "requestorcategory" : get_request_categories(),
                        "listing" : listing,
                        "watchlistIDs" : watchlistIDs,
                        "matchform" : matchform,
                        "is_requestor": is_requestor,
                        "commentform" : commentform,
                        "comments" : comments,
                        "requestor" : requestor
                    })

def requesting(request, requesting_id):
    donor=False
    requesting = Requesting.objects.get(id=requesting_id)
    comments = requesting.requestcomments.all().order_by("commentdate")
    form = SoldForm()
    commentform = CommentForm()
    try:
        watchlist = Watchlist.objects.filter(user=request.user)
    except:
        watchlist = ''
    watchlistIDs = [l.listing.id for l in watchlist]
    if requesting.sold == True:
        if requesting.donor == request.user:
            requestor = True
        else:
            requestor = False

    #if user is not logged in, shows text that user needs to be logged in to bid
    if request.user.is_authenticated == False:
        anonymous = True
        return render(request, "auctions/requesting.html", {
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
                "requesting" : requesting,
                "anonymous" : anonymous,
                "comments" : comments
            })
    #else authenticated users, split into owner of listing and not owner of listing
    else:
        if request.user == requesting.requestor:
            isOwner = True
        else:
            isOwner = False
        if (request.method == "POST" and 'commentsubmit' in request.POST):
            commentform = CommentForm(request.POST)
            commenttext = str(commentform.data["comment"])
            user = request.user
            newcomment = Comment(user=user, requesting=requesting, comment=commenttext, commentdate=timezone.localtime())
            newcomment.save()
            commentform = CommentForm()
        
        #if listing is viewed by the owner, show sold checkbox to take listing off the market but no bidding
        if isOwner:
            if (request.method == "POST" and 'soldsubmit' in request.POST):
                form = ExpireRequestForm(request.POST)
                soldValue = form.data["sold"]
                if soldValue == 'on':
                    sold = True
                requesting.sold = sold
                requesting.enddate = timezone.localtime()
                requesting.save()
                return render(request, "auctions/requesting.html", {
                    "categories" : get_categories(),
                    "requestorcategory" : get_request_categories(),
                    "requesting" : requesting,
                    "isOwner": isOwner,
                    "watchlistIDs" : watchlistIDs,
                    "commentform" : commentform,
                    "comments" : comments,
                    "requestor" : requestor
                })
            else:
                form = ExpireRequestForm()
                return render(request, "auctions/requesting.html", {
                    "categories" : get_categories(),
                    "requestorcategory" : get_request_categories(),
                    "requesting" : requesting,
                    "form" : form,
                    "isOwner": isOwner,
                    "watchlistIDs" : watchlistIDs,
                    "commentform" : commentform,
                    "comments" : comments,
                })
        #if requesting is viewed by a user who is not the donor, show request options
        else:
            anonymous = False
            return render(request, "auctions/requesting.html", {
                "categories" : get_categories(),
                "requestorcategory" : get_request_categories(),
                "requesting" : requesting,
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
    category = forms.ChoiceField(widget=forms.Select, choices=lambda: Category.objects.all().values_list('id', 'category'), label="Category", )
    price = forms.CharField(widget=forms.NumberInput(), label = "Estimated Donation Value")
    def clean_field(self):
        data = self.cleaned_data['imageurl']
        if data == '':
            data = 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png'
        return data
    error_css_class = 'error'
    required_css_class = 'font-weight-bold'

class RequestForm(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea,label="Description")
    imageurl = forms.CharField(widget=forms.URLInput(), label = "Image URL", required=False)
    requestorcategory = forms.ChoiceField(widget=forms.Select, choices=lambda: RequestorCategory.objects.all().values_list('id', 'category'), label="Category", )
    def clean_field(self):
        data = self.cleaned_data['imageurl']
        if data == '':
            data = 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Missing-image-232x150.png'
        return data
    error_css_class = 'error'
    required_css_class = 'font-weight-bold'    

class SoldForm(forms.Form):
    sold = forms.BooleanField(label="No longer donating?")

class ExpireRequestForm(forms.Form):
    sold = forms.BooleanField(label="Don't need item anymore?")

class RequestorMatch(forms.Form):
    match = forms.BooleanField(label="Request this item now?")

class DonorMatch(forms.Form):
    match = forms.BooleanField(label="Donate this item now?")
    value = forms.CharField(widget=forms.NumberInput(), label = "Estimated Donation Value")

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label="Add Comment")

class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname','lastname','school','address1','address2','city', 'state', 'zipcode', 'is_donor','is_requestor']