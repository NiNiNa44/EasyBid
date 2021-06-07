from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:cat>", views.index_cat, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:title>", views.listing_page, name="listing"),
    path("watchlist/<str:title>", views.watchlist, name="watchlist"),
    path("endbid/<str:title>", views.endbid, name="endbid"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page")
]
