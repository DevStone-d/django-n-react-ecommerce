# django-n-react-ecommerce
Django and React E-commerce project

## API ENDPOINTS

1. admin -> 256-bit key (g5as5kh6hv2jh5o8u4j5rtegd1) gibi

2. api/
    * collections/
        * add
        * delete/<slug>
        * detail/<slug>
    * products/
        * add
        * add/detail/<int:pk>
        * detail/<int:pk>
        * tag
        * tag/<slug>
        * status/<slug>
    * account/
        * profile
        * editprofile
    * rest-auth/
        * registration

3. api-auth/
    * login
    * logout


## ALL API ENDPOINTS

    api/collections
    api/collections/add
    api/collections/delete/<slug>
    api/collections/detail/<slug>

    api/products
    api/products/detail/<int:pk>
    api/products/add
    api/products/add/detail/<int:pk>
    api/products/tag
    api/products/tag/<slug>
    api/products/status/<slug>

    api/account/profile
    api/account/editprofile

    api/rest-auth/registration

    api-auth/login
    api-auth/logout



kargoya verilmeden adres degisikligi talebi olusturulabilir
giftboy.com hediyecim.com - online hediye gonderimi, steam code, vouchers, trendyol, zara alisveris karti


# Requirements API Calls 
### ADMIN CALLS
    api/products/delete/detail/<int:pk> -> delete the product's detail      OK
    api/products/edit/<slug>                                                OK
    api/products/edit/detail/<int:pk>                                       OK


    THESE FUTURE APIs MUST BE HAVE MODELS
    
###  USER CALLS
    api/cart -> user_token, cart.is_active
    api/cart/add
    api/cart/delete/<int:pk> -> delete one item
    api/cart/all/delete -> delete whole items from cart
    #3 gun sepet aktif, guest alisveris, sepette urunleriniz kaldi maili,odeme ekranina gelmeden bilgilerini alalim arka planda uyelik olussun

###  ADMIN CALLS
    api/campaigns
    api/campaigns/public -> allow any
    api/campaigns/detail/<int:pk> -> user auth

    api/campaigns/edit/<int:pk>
    api/campaigns/add
    api/campaigns/disable/<int:pk>
    api/campaigns/enable/<int:pk>
    api/campaigns/delete/<int:pk>
    
### ADMIN CALLS
    api/reviews
    api/reviews/all/<slug> -> Spesific Product's all reviews -> allow any
    api/reviews/<int:pk> -> Spesific User's all reviews
    api/reviews/<int:pk>/product/<slug> -> Spesific user's reviews on a specific product
    api/reviews/delete/<int:pk>

### USER CALLS
    api/account/reviews
    api/account/reviews/add/<slug>
    api/account/reviews/edit/<int:pk>
    api/account/reviews/delete/<int:pk>

    api/account/favorites
    api/account/favorites/add/<int:pk> -> look for product detail's pk
    api/account/favorites/delete/<int:pk>
    #kac kisi fav'a ekledi

    api/account/collections -> allow any, shareable
    api/account/collections/add -> user auth

    api/account/collections/delete/<slug> -> user auth
    api/account/collections/detail/<slug> -> allow any
    api/account/collections/detail/<slug>/product/add -> user auth, input: product 
    api/account/collections/detail/<slug>/product/delete -> user auth
    
### ADMIN CALLS
    api/site/log

## PERMS
    is_store
    is_delivery
    is_burhan
    is_editor
    is_staff
    is_accounting
    is_customerservice
    is_bakery


- Bunu da satin
- arama sonrasi sonuc yok
- arama gecmisi
- ürün çift variant 