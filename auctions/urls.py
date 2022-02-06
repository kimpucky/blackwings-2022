from django.urls import path
from . import views

urlpatterns = [
    path("", views.indexlisting, name="index"),
    path("indexrequesting", views.indexrequesting, name="indexrequesting"),
    path("category/<str:category>", views.category, name="category"),
    path("requestorcategory/<str:category>", views.requestorcategory, name="requestorcategory"),
    path("login", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile",views.profile, name="profile"),
    path("listing/donate", views.donate, name="donate"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("requesting/askfordonation/", views.askfordonation, name="askfordonation"),
    path("requesting/<int:requesting_id>", views.requesting, name="requesting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist")
]
