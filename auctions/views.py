from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import *
from django.core.exceptions import ObjectDoesNotExist

category = {
    "BOOKS": "Books",
    "ELECTRONICS": "Electronics",
    "FASHIONS": "Fashions",
    "HOME": "Home",
    "GAMES": "Games & Toys"
}


class BidForm(forms.Form):
    bid = forms.IntegerField(
        label="Bid Amount", min_value=0, max_value=999999999,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'start_bid', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'start_bid': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": "All Active Listing"
    })


def index_cat(request, cat):
    listings = Listing.objects.filter(active=True, category=cat)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category[cat]
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        if 'username' in request.POST and 'password' in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
                })
        else:
            return render(request, "auctions/login.html")

    else:
        return render(request, "auctions/login.html")


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
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing_page(request, title):
    listing = Listing.objects.get(title=title)
    form = BidForm()
    on_watchlist = True
    if not request.user.is_anonymous:
        try:
            Watchlist.objects.get(user=request.user, item=listing)
        except ObjectDoesNotExist:
            on_watchlist = False

    if request.method == 'POST':
        form = BidForm(request.POST)
        message = "success"

        if form.is_valid():
            try:
                bid = Bid.objects.get(user=request.user, listing=listing)
            except ObjectDoesNotExist:
                bid = Bid(user=request.user, listing=listing)

            bid_amount = form.cleaned_data['bid']
            if bid_amount > listing.price:
                bid.bid = bid_amount
                bid.save()
                listing.price = bid_amount
                listing.save()
            else:
                message = "error"

            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "form": form,
                "message": message,
                "on_watchlist": on_watchlist
            })

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "form": form,
        "on_watchlist": on_watchlist
    })


def watchlist(request, title):
    listing = Listing.objects.get(title=title)
    try:
        new_watchlist = Watchlist.objects.get(user=request.user)
    except ObjectDoesNotExist:
        new_watchlist = Watchlist.objects.create(user=request.user)
    if request.method == 'POST':
        watchlist_click = request.POST.get('watchlist')
        if watchlist_click == 'True':
            on_watchlist = True
            try:
                Watchlist.objects.get(user=request.user, item=listing)
            except ObjectDoesNotExist:
                on_watchlist = False
            if on_watchlist:
                new_watchlist.item.remove(listing)
            else:
                new_watchlist.item.add(listing)
    return HttpResponseRedirect(reverse("listing", args={title}))


def endbid(request, title):
    listing = Listing.objects.get(title=title)
    if request.method == 'POST':
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse("listing", args={title}))


def create_listing(request):
    form = ListingForm()
    message = "no"
    if request.method == 'POST':

        message = request.POST['title']
        new_listing = Listing(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            image=request.POST['image'],
            start_bid=request.POST['start_bid'],
            price=request.POST['start_bid'],
            category=request.POST['category']
        )
        new_listing.save()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def watchlist_page(request):
    try:
        user_watchlist = Watchlist.objects.get(user=request.user)
        listing = user_watchlist.item.all()
        return render(request, "auctions/index.html", {
            'listings': listing,
            'category': 'Watchlist'
        })
    except ObjectDoesNotExist:
        return render(request, "auctions/index.html", {
            'category': 'Watchlist'
        })











