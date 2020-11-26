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
    RetrieveUpdateDestroyAPIView,
)

from accounts.models import Account
from cart.models import Order,Cart,OrderedItem
from discounts.models import Coupon
from products.models import ProductDetail
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import CartListSerializer,OrderListSerializer,OrderedItemSerializer,CouponSerializer,CartDetailSerializer
from rest_framework import status

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
        #productId = request.data.get('slug',None) 
        #productId = lookup_field
        if productId is None:
            return Response({"message":"Invalid request"},status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(ProductDetail,id=productId)
        user = Account.objects.get(id=request.user.id)

        cart, created = Cart.objects.get_or_create(customer=user,ordered=False)       
        cart.save()     
        # quantity = int(request.data.get('quantity'))
        quantity = 1

        #if object is already in the cart
        # ordered_item, created_oitem = OrderedItem.objects.get_or_create(cart=cart,item=item,quantity=quantity)
        try:
            ordered_item = OrderedItem.objects.get(cart=cart,item=item)
            ordered_item.quantity += quantity
        except OrderedItem.DoesNotExist:
            ordered_item = OrderedItem(cart=cart,item=item,quantity=quantity)
        ordered_item.save()
        cart.total += item.price * quantity
        cart.discounted = cart.total ##
        cart.save()
        return Response(status=HTTP_200_OK)

class updateCart(RetrieveUpdateDestroyAPIView):
    queryset = OrderedItem.objects.all()
    lookup_field = 'pk'
    permission_classes = [AllowAny]
    serializer_class = OrderedItemSerializer

class addCoupon(RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CouponSerializer
    lookup_field = 'pk'

    def put(self, request, *args, **kwargs):
        serializer = CouponSerializer(data=request.data)
        if serializer.is_valid(request.data.get('id'),request.data.get('coupon'),request.user):
            serializer.update(request.data.get('id'))
            return Response({"message":"Coupon succesfully added"})
        else:
            return Response({"message":"ERROR"},status=status.HTTP_400_BAD_REQUEST)
            #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class userCart(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartDetailSerializer
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.filter(customer=user,ordered=False)
        return queryset




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

    cart.delete()
    # del cart
    # cart.save()

    return Response(status=HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def addaaaCoupon(request,code,pk):
    try:
        cart                = Cart.objects.get(id=pk)
        queryset            = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")
    cart                    = Cart.objects.filter(id=pk)
    cart.discounted = cart.total ##
    coupon = Coupon.objects.get_object_or_404(code=code)
    if coupon.customer is not None:
        if (request.user.id != coupon.customer.id):
            raise Http404("Coupon is not valid")
    if coupon.cart is not None:
        if (cart.id != coupon.cart.id):
            raise Http404("Coupon is not valid")
    if coupon.product is not None:
        items = OrderedItemSerializer(queryset,many=True).data
        item = 0
        for i in items:
            if (i.id == coupon.product.id):
                item = i
        if item == 0:
            raise Http404("Coupon is not valid")
      
    if coupon.coupon_type == '-1':
        raise Http404("Coupon is not valid")
    elif coupon.coupon_type == '0':
        cart.discounted -= cart.discounted/100*coupon.amount
        cart.save()
    elif coupon.coupon_type == '1':
        cart.discounted -= coupon.amount
        cart.save()
    elif coupon.coupon_type == '2':
        if cart.discounted >= coupon.above:
            cart.discounted = cart.discounted/100*coupon.amount
            cart.save()
        else:
            raise Http404("Coupon is not valid") #
    elif coupon.coupon_type == '3':
        if cart.discounted >= coupon.above:
            cart.discounted -= coupon.amount
            cart.save()
    elif coupon.coupon_type == 'p':
        cart.discounted -= (item.item.price - coupon.amount) * item.quantity
        cart.save()
    else:
        raise Http404("Coupon is not valid")

    # if cart.total != cart.discounted:
    #     coupon.limited -=1
    #     if coupon.limited == 0:
    #         coupon.is_active = 0
    #         coupon.delete()
    #     coupon.save()