from django.urls import path,include

<<<<<<< HEAD
from api.products.views import ProductList,ProductsTagList,productDetail,addProduct,addProductDetail,ProductsMediaList
=======
from api.products.views import ProductList,ProductsTagList,productDetail,addProduct,addProductDetail,ProductsMediaList,ProductStatus
>>>>>>> bedc2bebe8d4c7a7139e1f4b0e8c9da3d262e821
urlpatterns = [
    path('' ,  ProductList.as_view()  ,  name='products'),
    path('detail/<int:pk>/', productDetail , name='product detail'),
    path('add/', addProduct.as_view() , name='add product'),
    path('add/detail/<int:pk>/', addProductDetail , name='add product'),
<<<<<<< HEAD
=======
    path('status/<slug>/', ProductStatus.as_view() , name='product status'),
>>>>>>> bedc2bebe8d4c7a7139e1f4b0e8c9da3d262e821
    path('tags/',ProductsTagList.as_view()  ,  name='tag'),
    path('medias/',ProductsMediaList.as_view()  ,  name='media')
]