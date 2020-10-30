from django.urls import path,include

from api.collections.views import CollectionList,CollectionDetailList,addCollection,deleteCollection

urlpatterns = [
    path('' ,  CollectionList.as_view()  ,  name='collections'),
    path('add/',addCollection.as_view()  ,  name='addcollection'),
    path('detail/<slug>/',CollectionDetailList  ,  name='collection'),
    path('delete/<slug>/', deleteCollection.as_view() ,  name='deletecollection'),
    
]
