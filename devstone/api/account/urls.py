from django.urls import path
from . import views



urlpatterns = [
    path('profile/', views.getProfile ,name='getProfile'),
    path('editprofile/', views.AuthInfoUpdateView.as_view(),name='editProfile'),
    path('cart/', views.CartList.as_view() ,name='carts'),
    path('cart/<int:pk>', views.CartDetail ,name='getCart'),
]