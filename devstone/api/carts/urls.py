from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.CartList.as_view() ,name='carts'),
    #path('orders/', views.OrderList.as_view() ,name='orders'),
    path('add-to-cart/', views.AddToCart.as_view(), name="add-to-cart"),
    path('order-summary/', views.userCart.as_view(),name="order-summary"),
    path('clear-cart/<int:pk>', views.clearCart, name="clear-cart"),
    path('update-cart/<int:pk>', views.updateCart.as_view(), name="update-cart"),
    path('add-coupon/<int:pk>', views.addCoupon.as_view(), name="add-coupon"),
    path('detail/<int:pk>', views.CartDetail ,name='getCart')
]
