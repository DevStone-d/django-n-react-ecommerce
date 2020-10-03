from django.urls import path

from panel.api.views import api_detail_discount_view

app_name = 'panel'

urlpatterns = [
    path('discount/<code>/',api_detail_discount_view,name="detail"),
]


