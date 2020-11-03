# PERM AND USER RELATIONS 


## API AND USER RELATION : 

    class ProductAPIView(CreateAPIView) :

        def perform_create(self,serializer) :
            serializer.save( user = self.request.user )
            #serializer kaydedildikten sonra burada email gonderme islemi de yapilabilir.


    class ProductAPIView(UpdateAPIView) :

        def perform_update(self,serializer) :
            serializer.save( user = self.request.user )
            #serializer kaydedildikten sonra burada email gonderme islemi de yapilabilir.


    class ProductAPIView(DestroyAPIView) :

        def perform_destroy(self,serializer) :
            serializer.save( user = self.request.user )
            #serializer kaydedildikten sonra burada email gonderme islemi de yapilabilir.


## PERMISSIONS : 

### Rest Framework Default Permissions:
        from rest_framework.permissions import IsAuthenticated, IsAdminUser

####    Class Based Views :

            class ProductAPIView(CreateAPIView) :
                permissions_classes = [IsAuthenticated]
                def perform_create(self,serializer) :
                    serializer.save( user = self.request.user )
                    #serializer kaydedildikten sonra burada email gonderme islemi de yapilabilir.

####    Function Based Views : 
            @permission_classes([IsAuthenticated])
            @authentication_classes([SessionAuthentication, BasicAuthentication])
            def addProductDetail(request,pk):
                if request.method == 'GET':
                    try:
                        xproduct        = Product.objects.filter(id=pk)
                        product         = Product.objects.get(id=pk)
                    except Product.DoesNotExist:
                        data            = {'detail':'Parent Product does not exist'}
                        return Response(data)

                    productDetail       = ProductDetail.objects.filter(product=product)

    
### Custom Permissions : 

        1. Create new file in your general api folder or specific api folder. This file's name should be permissions.py
        2. Import 'BasePermission' package from rest_framework.permissions
            from rest_framework.permissions import BasePermission

        3. You should be write your class like this : 

            class IsStore(BasePermission) :
                def has_object_permission(self,request,view,obj):
                    return request.user.IsStore

                def has_permission(self,request):
                    return request.user.IsStore

        4. You can write your message like this if your user has not this permission : 

            class IsStore(BasePermission) :
                message = 'You have not permission for this request.'
                def has_object_permission(self,request,view,obj):
                    return request.user.IsStore

                def has_permission(self,request):
                    return request.user.IsStore

        Notes : 

            has_object_permission ------ work with a request type
            has_permission        ------ work with a GET requests




