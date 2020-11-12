from django.shortcuts import render
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from accounts.models import Order,Cart,OrderedItem
from products.models import ProductDetail
from rest_framework.permissions import IsAuthenticated,AllowAny

from api.account.serializers import OrderedItemSerializer
from .serializers import CartListSerializer,OrderListSerializer
# Create your views here.
class CartList(ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [AllowAny]

class OrderList(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]

class AddToCart(APIView):
    queryset = OrderedItem.objects.all()
    lookup_field = 'pk'
    permission_classes = [AllowAny]
    serializer_class = OrderedItemSerializer

    def post(self,request,*args,**kwargs):
        productId = request.data.get('item',None)
        if productId is None:
            return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(ProductDetail,id=productId)

        cart, created = Cart.objects.get_or_create(customer=request.user.id,ordered=False)

        quantity = request.data.get('quantity')

        #if object is already in the cart
        ordered_item, created_oitem = OrderedItem.objects.get_or_create(cart=cart,item=item,quantity=quantity)
        if created_oitem:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity

        
        return Response(status=HTTP_200_OK)
