from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth.decorators import login_required


from accounts.models import Account
from panel.models import Discount
from products.models import Product,ProductDetail,ProductMedia,Tag

from products.api.serializers import ProductSerializer,ProductDetailSerializer,ProductMediaSerializer,TagSerializer


@api_view(['GET',])
def api_detail_product_view(request,meta_url):
    try:
        product = Product.objects.get(meta_url=meta_url)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET": 
        serializer = ProductSerializer(product)
        return Response(serializer.data)