from django.urls import path
from . import views

urlpatterns = [
    path('create-customer/', views.createCustomer.as_view(), name="create-customer"),
    path('profile/', views.getProfile ,name='getProfile'),
    path('editprofile/', views.AuthInfoUpdateView.as_view(),name='editProfile'),
    # path('cart/<int:pk>', views.CartDetail ,name='getCart'),
]