from rest_framework import serializers
from products.models import Product,ProductDetail,ProductMedia,Tag

class ListProductsAPIView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'description',
            'video_url',
            'slug',
            'meta_desc'
        ]

class ListProductDetailAPIView(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            'id',
            'product',
            'first_price',
            'price',
            'stock',
            'variant',
            'variable'
        ]

class ListProductMediaAPIView(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = [
            'id',
            'product',
            'image_url',
        ]

class ListProductTagAPIView(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'product',
            'tag',
        ]
# kampanyalar
#     - kategori kampanyalari
#     - urun kampanyalari
#     - user kampanyalari
#     - kod kampanyalari