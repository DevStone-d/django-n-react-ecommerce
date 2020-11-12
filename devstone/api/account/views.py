from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from api.permissions import (
    IsStore,
    IsDelivery,
    IsBurhan,
    IsEditor,
    IsStaff,
    IsAccounting,
    IsCustomerService,
    IsBakery
)
from api.account.serializers import AccountDetailSerializer,UserSerializer,OrderedItemSerializer
from api.serializers import CartListSerializer, OrderListSerializer
from accounts.models import Account,Order,Cart,OrderedItem
from products.models import ProductDetail

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

@api_view(['GET',])
def index(request):
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET',])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getProfile(request):
    if request.method == "GET":
        user = request.user
        serializer = AccountDetailSerializer(user)
        return Response(serializer.data)


class AuthInfoUpdateView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = UserSerializer
    
    queryset = Account.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(usermail=request.user.email)
            return Response({"message":"Profile succesfully update"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def CartDetail(request,pk):
    try:
        cart        = Cart.objects.get(id=pk)
        queryset    = OrderedItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        data            = {'detail':'Cart does not exist'}
        return Response(data)

    cart                = Cart.objects.filter(id=pk)

    cartSerializer      = CartListSerializer(cart,many=True)
    oProductsSerializer = OrderedItemSerializer(queryset,many=True)

    responsibleData = {}
    responsibleData['cart']             =  cartSerializer.data
    responsibleData['ordered products'] =  oProductsSerializer.data

    return Response(responsibleData)

        

        
