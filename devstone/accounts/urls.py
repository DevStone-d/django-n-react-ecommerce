from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name='users'
urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("orders", views.orders, name="orders"),
    path("reviews", views.reviews, name="reviews"),
    path("adress", views.adress, name="adress"),
    path("changePass", views.changePass, name="changePass"),
    path("adressdelete/<int:id>", views.adressdelete, name="adressdelete"),
    
]