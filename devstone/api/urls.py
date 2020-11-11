from django.urls import path,include
from . import views

urlpatterns = [
    path('collections/',include('api.collections.urls')),
    path('products/',include('api.products.urls')),   
    path('account/', include('api.account.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('carts/', views.CartList.as_view() ,name='carts'),
    path('orders/', views.OrderList.as_view() ,name='orders'),
    path('add-to-cart/<int:id>', views.AddToCart.as_view(), name="add-to-cart")
]
