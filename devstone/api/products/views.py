from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView
from rest_framework.response import Response

#our serializers
from api.products.serializers import ListProductsAPIView,ListProductDetailAPIView, ListProductMediaAPIView,ListProductTagAPIView

#models
from products.models import Collection, Product, ProductDetail, ProductMedia , Tag

class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ListProductsAPIView

class ProductsTagList(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = ListProductTagAPIView


class ProductDetailList(ListAPIView):
    # queryset = ProductDetail.objects.all()
    serializer_class = ListProductDetailAPIView
    # lookup_field = "pk"
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = ProductDetail.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = ProductDetail.objects.filter(pk=0)
            return queryset
        return queryset

class ProductMediaList(ListAPIView):
    serializer_class = ListProductMediaAPIView
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = ProductMedia.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = ProductMedia.objects.filter(pk=0)
            return queryset
        return queryset

class ProductTagList(ListAPIView):
    serializer_class = ListProductTagAPIView
    def get_queryset(self):
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            queryset = Tag.objects.filter(product=product)
        except Product.DoesNotExist:
            queryset = Tag.objects.filter(pk=0)
            return queryset
        return queryset