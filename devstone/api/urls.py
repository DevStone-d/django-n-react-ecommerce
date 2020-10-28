from django.urls import path,include


urlpatterns = [
    path('collections/',include('api.collections.urls')),
    path('products/',include('api.products.urls')),   
    path('account/', include('api.account.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]
