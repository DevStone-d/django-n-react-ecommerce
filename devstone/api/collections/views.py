from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView
from rest_framework.response import Response

#our serializers
from api.collections.serializers import ListCollectionsAPIView,ListCollectionDetailAPIView

#models
from products.models import Collection, Product

class CollectionList(ListAPIView):
    queryset = Collection.objects.all()
    serializer_class = ListCollectionsAPIView


class CollectionDetailList(ListAPIView):
    serializer_class = ListCollectionDetailAPIView
    def get_queryset(self):
        try:
            category = Collection.objects.get(slug=self.kwargs['category'])
            queryset = Product.objects.filter(category=category)
        except Collection.DoesNotExist:
            queryset = Product.objects.filter(pk=0)
            return queryset
        return queryset

        

        
        