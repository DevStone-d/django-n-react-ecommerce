from rest_framework import serializers
from products.models import Collection,Product

class ListCollectionsAPIView(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            'name',
            'img',
            'description',
            'slug',
            'meta_desc'
        ]

class ListCollectionDetailAPIView(serializers.ModelSerializer):
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