from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_200_OK
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)

from cart.models import Order,Cart,OrderedItem
from products.models import ProductDetail
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import CartListSerializer,OrderListSerializer,OrderedItemSerializer

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
    # queryset = OrderedItem.objects.all()
    # lookup_field = 'pk'
    # permission_classes = [AllowAny]
    # serializer_class = OrderedItemSerializer

    def post(self,request,*args,**kwargs):
        productId = request.data.get('item',None)
        #productId = request.data.get('slug',None) 
        #productId = lookup_field
        if productId is None:
            return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(ProductDetail,id=productId)

        cart, created = Cart.objects.get_or_create(customer=request.user.id,ordered=False)

        quantity = int(request.data.get('quantity'))

        #if object is already in the cart
        ordered_item, created_oitem = OrderedItem.objects.get_or_create(cart=cart,item=item,quantity=quantity)
        if created_oitem:
            ordered_item.quantity = quantity
        else:
            ordered_item.quantity += quantity
        ordered_item.save()
        cart.total += item.price * quantity
        cart.save()
        return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def CartDetail(request,pk):
    try:
        cart        = Cart.objects.get(id=pk)
        queryset    = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # data            = {'detail':'Cart does not exist'}
        # return Response(data)
        # return Response({"message":"Cart does not exist"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Cart does not exist")

    cart                = Cart.objects.filter(id=pk)

    cartSerializer      = CartListSerializer(cart,many=True)
    oProductsSerializer = OrderedItemSerializer(queryset,many=True)

    responsibleData = {}
    responsibleData['cart']             =  cartSerializer.data
    responsibleData['ordered products'] =  oProductsSerializer.data

    return Response(responsibleData)

@api_view(['GET'])
@permission_classes([AllowAny])
def clearCart(request,pk):
    try:
        cart        = Cart.objects.get(id=pk)
        queryset    = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # data            = {'detail':'Cart does not exist'}
        # return Response(data)
        raise Http404("Cart does not exist")

    cart                = Cart.objects.filter(id=pk)

    # cart.delete()
    # del cart
    # cart.save()

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def updateCart(request,pk):
    try:
        cart                = Cart.objects.get(id=pk)
        queryset            = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # return Response({"message":"Cart does not exist"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Cart does not exist")
    cart                    = Cart.objects.filter(id=pk)
    productId               = request.data.get('item',None)
    if productId is None:
        # return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Invalid request")
    item                    = get_object_or_404(ProductDetail,id=productId)
    quantity                = int(request.data.get('quantity')) #input quantity
    ordered_item            = OrderedItem.objects.get(cart=cart,item=item) # get the item
    cart.total             -= item.price * ordered_item.quantity # cart'tan itemin ucretini cikariyoruz, yani item adetini 0'a indiriyoruz gibi bir sey
    ordered_item.quantity   = quantity # item's new quantity
    ordered_item.save()
    cart.total             += item.price * quantity # add item's price * quantity to the cart total
    cart.save()

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def plus1Cart(request,pk):
    try:
        cart                = Cart.objects.get(id=pk)
        queryset            = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # return Response({"message":"Cart does not exist"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Cart does not exist")
        
    cart                    = Cart.objects.filter(id=pk)
    productId               = request.data.get('item',None)
    if productId is None:
        # return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Invalid request")
    item                    = get_object_or_404(ProductDetail,id=productId)
    ordered_item            = OrderedItem.objects.get(cart=cart,item=item) # get the item
    ordered_item.quantity   += 1 # item's new quantity
    ordered_item.save()
    cart.total             += item.price # add item's price * quantity to the cart total
    cart.save()

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def minus1Cart(request,pk):
    try:
        cart                = Cart.objects.get(id=pk)
        queryset            = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # return Response({"message":"Cart does not exist"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Cart does not exist")
    cart                    = Cart.objects.filter(id=pk)
    productId               = request.data.get('item',None)
    if productId is None:
        # return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Invalid request")
    item                    = get_object_or_404(ProductDetail,id=productId)
    ordered_item            = OrderedItem.objects.get(cart=cart,item=item) # get the item
    if ordered_item.quantity == 1:
        ordered_item.delete()
    else:
        ordered_item.quantity   -= 1 # item's new quantity
        ordered_item.save()
    cart.total             -= item.price # add item's price * quantity to the cart total
    cart.save()

    return Response(status=HTTP_200_OK)

def addCoupon(request,code,pk):
    try:
        cart                = Cart.objects.get(id=pk)
        queryset            = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        # return Response({"message":"Cart does not exist"},status=HTTP_400_BAD_REQUEST)
        raise Http404("Cart does not exist")
    cart                    = Cart.objects.filter(id=pk)