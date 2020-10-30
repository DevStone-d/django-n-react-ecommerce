from django.urls import path,include

from api.products.views import ProductList, ProductDetailList, ProductMediaList,ProductTagList,ProductsTagList,productDetail,addProduct,addProductDetail

urlpatterns = [
    path('' ,  ProductList.as_view()  ,  name='products'),
    path('detail/<int:pk>/', productDetail , name='product detail'),
    path('add/', addProduct.as_view() , name='add product'),
    path('add/detail/<int:pk>/', addProductDetail , name='add product'),
    #path('detail/<slug>',ProductDetailList.as_view()  ,  name='product'),
    path('media/<slug>',ProductMediaList.as_view()  ,  name='media'),
    path('tag/',ProductsTagList.as_view()  ,  name='tag'),
    path('tag/<slug>',ProductTagList.as_view()  ,  name='tag'),
]