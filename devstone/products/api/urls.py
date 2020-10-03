from django.urls import path

from products.api.views import api_detail_product_view

app_name = 'products'

urlpatterns = [
    path('<meta_url>/',api_detail_product_view,name="detail"),
]


