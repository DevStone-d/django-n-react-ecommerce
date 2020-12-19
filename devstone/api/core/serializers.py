from rest_framework import serializers

from core.models import SiteMap,Categories,SiteMapItem

from products.models import Collection



class FullSiteMap(serializers.ModelSerializer):
    submenus = serializers.SerializerMethodField()
    class Meta:
        model = SiteMapItem
        fields = [
            'id',
            'title',
            'relationalModel',
            'url',
            'submenus',
            'haveChild',
            'haveParent'
        ]
    def get_submenus(self,obj):
        childList = []
        submenus = SiteMap.objects.filter(parentItem=obj.id)
        for i in submenus:
            currentChild = SiteMapItem.objects.get(id=i.childItem.id)
            newDict = {
                    'id'    : currentChild.id,
                    'key'   : currentChild.relationalModel,
                    'title' : currentChild.title,
                    'url'   : currentChild.url,
                    'haveChild': currentChild.haveChild,
                    'haveParent':currentChild.haveParent
                }
            if currentChild.haveParent:
                childList2 = []
                submenus2 = SiteMap.objects.filter(parentItem=currentChild.id)
                for j in submenus2:
                    currentChild = SiteMapItem.objects.get(id=j.childItem.id)
                    newDict2 = {
                            'id'    : currentChild.id,
                            'key'   : currentChild.relationalModel,
                            'title' : currentChild.title,
                            'url'   : currentChild.url,
                            'haveChild': currentChild.haveChild,
                            'haveParent':currentChild.haveParent,
                            'submenus' : []
                        }
                    childList2.append(newDict2)
                newDict['submenus'] = childList2
            childList.append(newDict)
        return childList
    
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
    
    