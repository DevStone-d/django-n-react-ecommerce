from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView,DestroyAPIView,RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

#our serializers
from api.collections.serializers import ListCollectionsAPIView,CollectionDetailAPIView

#models
from products.models import Collection, Product

#custom perms
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

class CollectionList(ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = ListCollectionsAPIView
    permission_classes = [AllowAny]

class CollectionDetail(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CollectionDetailAPIView
    queryset = Collection.objects.all()
    lookup_field = 'slug'
    
class addCollection(ListCreateAPIView):
    permission_classes = [IsEditor,IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListCollectionsAPIView
    queryset = Collection.objects.all()

class deleteCollection(RetrieveDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListCollectionsAPIView
    queryset = Collection.objects.all()
    lookup_field = 'slug'
