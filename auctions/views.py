from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import *
from .models import Bid, Comment, Listing, User


def index(request):
    return render(request, "auctions/index.html", {
        "active_listings": Listing.objects.filter(active=True)
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def update_bid(bid, listing):
    if listing.current_bid is None:
        if bid.amount > listing.starting_bid:
            return True
    else:
        if bid.amount > listing.current_bid:
            return True
    return False


def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
    except Listing.DoesNotExist:
        raise Http404("Listing does not exist")
    if request.method == "POST":
        user = request.user
        bid_form = CreateBidForm(request.POST)
        comment_form = CreateCommentForm(request.POST)
        if 'start_watching' in request.POST:
            listing.watchers.add(user)
        elif 'stop_watching' in request.POST:
            listing.watchers.remove(user)
        if 'amount' in request.POST:
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                if update_bid(bid,listing):
                    bid.user = request.user
                    bid.listing = listing
                    bid.save()
                    listing.current_bid = bid.amount
                    listing.save()
        if 'comment' in request.POST:
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = user
                comment.listing = listing
                comment.save()
        return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
    return render(request, "auctions/listing.html", {
            "listing": listing,
            "seller": str(listing.seller).capitalize(),
            "item_name": listing.item_name,
            "description": listing.description,
            "category": listing.category,
            "photo": listing.photo,
            "deadline": listing.deadline,
            "starting_bid": listing.starting_bid,
            "current_bid": listing.current_bid,
            "watchers": listing.watchers,
            "bid_form": CreateBidForm(),
            "comment_form": CreateCommentForm(),
            "comments":listing.comments.all()
        })

def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/create.html", {
                "form":form
            })
    return render(request, "auctions/create.html", {
        "form": CreateListingForm()
    })

def get_watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "watchlist": watchlist
    })


def add_comment(request):
    comment_form = CreateCommentForm(request.POST)
