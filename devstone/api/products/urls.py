from django.urls import path,include

from api.products.views import (ProductList,
                                ProductsTagList,
                                addProduct,
                                addProductDetail,
                                ProductsMediaList,
                                ProductStatus,
                                DeleteProductDetail,
                                EditProduct,
                                EditProductDetail,
                                getProductDetail,
                                )

urlpatterns = [
    path('' ,  ProductList.as_view()  ,  name='products'),
    path('detail/<int:id>/', getProductDetail.as_view() , name='product detail'),
    path('add/', addProduct.as_view() , name='add product'),
    path('add/detail/<int:pk>/', addProductDetail , name='add product'),
    path('status/<slug>/', ProductStatus.as_view() , name='product status'),
    path('tags/',ProductsTagList.as_view()  ,  name='tag'),
    path('medias/',ProductsMediaList.as_view()  ,  name='media'),
    path('delete/detail/<int:pk>',DeleteProductDetail.as_view(),name='delete product detail'),
    path('edit/<slug>',EditProduct.as_view(),name='edit product'),
    path('edit/detail/<int:pk>',EditProductDetail.as_view(),name='edit product'),


]