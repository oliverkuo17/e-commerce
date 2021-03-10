from django.urls import path

from . import views

app_name = "auctions"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing_view, name="listing"),
    path("listings/create", views.create_listing, name="create_listing"),
    path("watchlist", views.get_watchlist, name="get_watchlist"),
    # path("category/<str:category_name>", views.category, name="category")
]
