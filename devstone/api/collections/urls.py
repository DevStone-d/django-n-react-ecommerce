from django.urls import path,include

from api.collections.views import CollectionList,CollectionDetailList

urlpatterns = [
    path('' ,  CollectionList.as_view()  ,  name='collections'),
    path('<category>',CollectionDetailList.as_view()  ,  name='collection'),
]
