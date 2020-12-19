from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView,DestroyAPIView,RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import SessionAuthentication,BasicAuthentication

#our serializers
from products.models import Collection
from core.models import Categories,SiteMapItem
from api.core.serializers import DetailCollectionList,FullSiteMap



class getList(ListAPIView):
    serializer_class        = DetailCollectionList
    permission_classes      = [AllowAny]
    
    def get_queryset(self):
        
        slug = self.kwargs['slug']
        if slug is not None:
            
            try:
                category            = Collection.objects.get(slug=slug)
                queryset            = Categories.objects.all()
                queryset = queryset.filter(parent=category.id)
            except:
                queryset = Collection.objects.filter(slug=slug)
            
        
        return queryset

class getFullSiteMap(ListAPIView):
    serializer_class        = FullSiteMap
    permission_classes      = [AllowAny]
    queryset                = SiteMapItem.objects.filter(haveParent=False)