from rest_framework import serializers

from products.models import Product,ProductDetail,ProductMedia,Tag


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "category",  
            "name",
            "description",
            "video_url",
            "meta_url",
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = [
            "product_detail_id"
            "product_id",
            "first_price",  
            "price",
            "stock",
            "variant",
            "variable",
        ]

class ProductMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = [
            "product_media_id"
            "product_detail_id",
            "image_url",
        ]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "tag_id"
            "product_detail_id",
            "tag",
        ]
