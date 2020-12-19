from django.urls import path,include

from api.core.views import getList,getFullSiteMap

urlpatterns = [
    path('' ,  getFullSiteMap.as_view()  ,  name='sitemap'),
    path('collections/<slug>',getList.as_view()  ,  name='deneme'),
    # path('add/',addCollection.as_view()  ,  name='addcollection'),
    # path('delete/<slug>/', deleteCollection.as_view() ,  name='deletecollection'),
    # path('update/<slug>/', deleteCollection.as_view() ,  name='deletecollection'),
]
