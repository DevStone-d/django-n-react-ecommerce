from rest_framework import serializers
from products.models import Collection,Product
from api.products.serializers import ListProductsAPIView

class ListCollectionsAPIView(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'id',
            'name',
            'img',
            'description',
            'slug',
            'meta_desc'
        ]
class CollectionDetailAPIView(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Collection
        fields = [
            'id',
            'name',
            'img',
            'description',
            'slug',
            'meta_desc',
            'products'
        ]
    def get_products(self,obj):
        queryset            = Product.objects.filter(category=obj.id)
        productsSerializer  = ListProductsAPIView(queryset,many=True).data
        return productsSerializer