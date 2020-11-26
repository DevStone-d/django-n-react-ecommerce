from rest_framework import serializers
from products.models import Product,ProductDetail,ProductMedia,Tag

class ListProductsAPIView(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'description',
            'video_url',
            'slug',
            'thumbnail',
            'meta_desc',
            'is_active'
        ]
    def get_category(self,obj):
        categorylist = []
        for i in obj.category.all():
            categorylist.append(i.name)
        return categorylist
class ListProductTagAPIView(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'id',
            'product',
            'tag',
        ]

class ListProductDetailAPIView(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            'id',
            '__str__',
            'first_price',
            'price',
            'stock',
            'variant',
            'variable',
            'thumbnail'
        ]
class ListProductMediaAPIView(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = [
            'id',
            'product',
            'image_url',
        ]
        
class DetailProductAPIView(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    variants = serializers.SerializerMethodField()
    medias = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id',
            'category',
            'name',
            'description',
            'video_url',
            'slug',
            'thumbnail',
            'meta_desc',
            'is_active',
            'variants',
            'medias',
            'tags'
        ]
    def get_category(self,obj):
        categorylist = []
        for i in obj.category.all():
            categorylist.append(i.name)
        return categorylist
    def get_variants(self,obj):
        queryset            = ProductDetail.objects.filter(product=obj.id)
        productDetailSeri   = ListProductDetailAPIView(queryset,many=True).data
        return productDetailSeri
    def get_medias(self,obj):
        queryset            = ProductMedia.objects.filter(product=obj.id)
        productMediaSeri    = ListProductMediaAPIView(queryset,many=True).data
        return productMediaSeri
        
    def get_tags(self,obj):
        queryset            = Tag.objects.filter(product=obj.id)
        productTagSeri      = ListProductTagAPIView(queryset,many=True).data
        return productTagSeri
        
class ProductStatusAPIView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'slug',
            'is_active'
        ]









#     - kategori kampanyalari
#     - urun kampanyalari
#     - user kampanyalari
#     - kod kampanyalari