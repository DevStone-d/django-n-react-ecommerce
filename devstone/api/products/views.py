from django.shortcuts import render


from rest_framework.generics import ListAPIView,RetrieveAPIView,ListCreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.authentication import BasicAuthentication,SessionAuthentication, TokenAuthentication
#our serializers
from api.products.serializers import ListProductsAPIView,ListProductDetailAPIView, ListProductMediaAPIView,ListProductTagAPIView, ProductStatusAPIView

#models
from products.models import Collection, Product, ProductDetail, ProductMedia , Tag
#custom permissions
from api.permissions import (
    IsStore,
    IsDelivery,
    IsBurhan,
    IsEditor,
    IsStaff,
    IsAccounting,
    IsCustomerService,
    IsBakery
)

class addProduct(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ListProductsAPIView
    permission_classes = [IsEditor,IsAdminUser]
    queryset = Product.objects.all()
    

@api_view(['POST','GET'])
@permission_classes([IsEditor,IsAdminUser])
@authentication_classes([SessionAuthentication, BasicAuthentication]) # +TokenAuthentication
def addProductDetail(request,pk):
    if request.method == 'GET':
        try:
            xproduct        = Product.objects.filter(id=pk)
            product         = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            data            = {'detail':'Parent Product does not exist'}
            return Response(data)

        productDetail       = ProductDetail.objects.filter(product=product)

        productSeri         = ListProductsAPIView(xproduct,many=True)
        productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)

        responsibleData = {}
        responsibleData['product']  = productSeri.data
        responsibleData['variants'] = productDetailSeri.data

        return Response(responsibleData)

    if request.method == 'POST':
        try:
            parentProduct   = Product.objects.get(id=request.data['product'])
            parentProduct   = Product.objects.filter(id=request.data['product'])
        except Product.DoesNotExist:
            data            = {'detail':'Parent product does not exist'}
            return Response(data)

        productSerializer = ListProductDetailAPIView(data=request.data)

        if request.data['product'] != pk :
            data            = {'detail':'Invalid operation'}
            return Response(data)

        if productSerializer.is_valid():
            productSerializer.save()
            try:
                xproduct        = Product.objects.filter(id=pk)
                product         = Product.objects.get(id=pk)
            except Product.DoesNotExist:
                data            = {'detail':'Parent Product does not exist'}
                return Response(data)

            productDetail       = ProductDetail.objects.filter(product=product)

            productSeri         = ListProductsAPIView(xproduct,many=True)
            productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)

            responsibleData = {}
            responsibleData['message']  = "Product's Detail succesfully created."
            responsibleData['product']  = productSeri.data
            responsibleData['variants'] = productDetailSeri.data

            return Response(responsibleData)
        else:
            data            = {'detail':'error'}
            return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def productDetail(request,pk):
    try:
        xproduct        = Product.objects.filter(id=pk)
        product         = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        data            = {'detail':'Product does not exist'}
        return Response(data)

    productDetail       = ProductDetail.objects.filter(product=product)
    productMedia        = ProductMedia.objects.filter(product=product)
    productTag          = Tag.objects.filter(product=product)

    productSeri         = ListProductsAPIView(xproduct,many=True)
    productDetailSeri   = ListProductDetailAPIView(productDetail,many=True)
    productMediaSeri    = ListProductMediaAPIView(productMedia,many=True)
    productTagSeri      = ListProductTagAPIView(productTag,many=True)

    responsibleData = {}
    responsibleData['product'] = productSeri.data
    responsibleData['variants'] = productDetailSeri.data
    responsibleData['medias'] = productMediaSeri.data
    responsibleData['tags']   = productTagSeri.data

    return Response(responsibleData)


# class ProductDisable(RetrieveUpdateAPIView):
#     queryset = Product.objects.all()
#     permission_classes = [IsAdminUser]
#     serializer_class = ProductDisableAPIView
#     lookup_field = "slug"
#     def perform_update(self, serializer):
#         serializer.save(is_active=False)
#         return super().perform_update(serializer)

# class ProductDisable(RetrieveDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     serializer_class = ProductDisableAPIView
#     queryset = Product.objects.all()
#     lookup_field = 'slug'
#     def perform_destroy(self, serializer):
#         serializer.is_active = False
#         serializer.save()
#         return serializer

class ProductStatus(RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = ProductStatusAPIView
    queryset = Product.objects.all()
    lookup_field = 'slug'


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]

    serializer_class = ListProductsAPIView

class ProductsTagList(ListAPIView):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListProductTagAPIView

class ProductsMediaList(ListAPIView):
    queryset = ProductMedia.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ListProductMediaAPIView

