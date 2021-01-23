from accounts.models import Customer
from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
)
# # Create your views here.


from api.account.serializers import AccountDetailSerializer,UserSerializer,GuestCustomerSerializer

from accounts.models import Account
from products.models import ProductDetail

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
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    def put(self, request, *args, **kwargs):
        serializer = AccountDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(usermail=request.user.email)
            return Response({"message":"Profile succesfully update"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class createCustomer(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = GuestCustomerSerializer
    queryset = Customer.objects.all()
