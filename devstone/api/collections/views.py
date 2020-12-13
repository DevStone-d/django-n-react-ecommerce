from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView,DestroyAPIView,RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

#our serializers
from api.collections.serializers import ListCollectionsAPIView,CollectionDetailAPIView
from api.products.serializers import DetailProductAPIView
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
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = CollectionDetailAPIView
    queryset = Collection.objects.all()
    lookup_field = 'slug'

class CollectionProductList(ListAPIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = DetailProductAPIView
    lookup_field = 'slug'
    
    def get_queryset(self):
        catSlug = self.kwargs['slug']
        try:
            xcat        = Collection.objects.filter(slug=catSlug)
            cat         = Collection.objects.get(slug=catSlug)
        except Product.DoesNotExist:
            data            = {'detail':'Parent Product does not exist'}
            return Response(data)
        queryset            = Product.objects.filter(category=cat)


        return queryset

# class getProductDetail(ListAPIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     serializer_class = DetailProductAPIView
#     permission_classes = [AllowAny]
#     lookup_field = "id"
#     queryset = Product.objects.all()


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
