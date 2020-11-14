from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.CartList.as_view() ,name='carts'),
    #path('orders/', views.OrderList.as_view() ,name='orders'),
    path('add-to-cart/<int:id>', views.AddToCart.as_view(), name="add-to-cart"),
    path('<int:pk>', views.CartDetail ,name='getCart')
]
