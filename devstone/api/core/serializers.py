from rest_framework import serializers

from core.models import Categories,SiteMapItem

from products.models import Collection


class SiteMapSerializer(serializers.ModelSerializer):
    submenus = serializers.SerializerMethodField()
    class Meta:
        model = SiteMapItem
        fields = [
            'id',
            'title',
            'relationalModel',
            'url',
            'haveParent',
            'submenus',
            'priority'
        ]
    def get_submenus(self,obj):
        queryset  = SiteMapItem.objects.filter(parent=obj.id).order_by("priority")
        serial    = SiteMapSerializer(queryset,many=True).data
        return serial
    
class DetailCollectionList(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    child  = serializers.SerializerMethodField()
    class Meta:
        model = Categories
        fields = [
            'parent',
            'haveChild',
            'child'
        ]
    def get_parent(self,obj):
        parentCollection = Collection.objects.get(id=obj.parent.id)
        newDict = {
                'id'    : parentCollection.id,
                'name'  : parentCollection.name,
                'img'   : parentCollection.img,
                'slug'  : parentCollection.slug
            }
        return newDict
    def get_child(self,obj):
        if obj.haveChild:
            childCollection = Collection.objects.get(id=obj.child.id)
            newDict = {
                    'id'    : childCollection.id,
                    'name'  : childCollection.name,
                    'img'   : childCollection.img,
                    'slug'  : childCollection.slug
                }
            return newDict
        return obj.child
    
    