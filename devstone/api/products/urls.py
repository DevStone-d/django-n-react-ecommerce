from django.urls import path,include

from api.products.views import ProductList,ProductsTagList,productDetail,addProduct,addProductDetail,ProductsMediaList,ProductStatus
urlpatterns = [
    path('' ,  ProductList.as_view()  ,  name='products'),
    path('detail/<int:pk>/', productDetail , name='product detail'),
    path('add/', addProduct.as_view() , name='add product'),
    path('add/detail/<int:pk>/', addProductDetail , name='add product'),
    path('status/<slug>/', ProductStatus.as_view() , name='product status'),
    path('tags/',ProductsTagList.as_view()  ,  name='tag'),
    path('medias/',ProductsMediaList.as_view()  ,  name='media')
]