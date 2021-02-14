from rest_framework import serializers
from cart.models import Cart,Order,OrderedItem
from rest_auth.serializers import UserDetailsSerializer
from products.models import Product,ProductDetail
from django.http import Http404
from django.shortcuts import get_object_or_404
from discounts.models import Coupon
from accounts.models import Customer


import json

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance



class GuestCartSerializer(serializers.Serializer):
    email           = serializers.EmailField()
    ordered_items   = serializers.JSONField()
    """
    ordered_items = {
        item : 28
        quantity : 1
    }
    item : ProductDetail.id(unique)
    """
    # def create(self, validated_data):
    #     """
    #     Create and return a new `Snippet` instance, given the validated data.
    #     """
    #     return Snippet.objects.create(**validated_data)
    

    def get_or_create_customer(self,email):
        customer, created = Customer.objects.get_or_create(email=email)
        customer.save()
        return customer

    def get_or_create_cart(self,customer):
        try :
            cart = Cart.objects.get(customer=customer,ordered=False)
            cart.delete()
        except :
            pass
        cart = Cart(customer=customer,ordered=False)
        cart.save()
        return cart

    def create_ordered_item(self,ordered_item):
        try :
            item = ProductDetail.objects.get(id=int(ordered_item["item"]))
            orderedItem = OrderedItem(cart = self.cart, item = item, quantity = int(ordered_item["quantity"]))
            orderedItem.save()
        except:
            pass
    def create_ordered_items(self,ordered_items,email):
        customer = self.get_or_create_customer(email)
        self.cart = self.get_or_create_cart(customer)
        ordered_items = json.loads(ordered_items) #SERIALIZER PROBLEMLİ
        for ordered_item in ordered_items:
            self.create_ordered_item(ordered_item = ordered_item)


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 
            'cart', 
            'address', 
            'created',
            'status',
            'amount',
            ]
class OrderedItemSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = OrderedItem
        fields = [
            'id', 
            'cart', 
            'item',
            'order_items',
            'quantity',
            'item_total'
            ]
    def get_order_items(self,obj):
        mydick = {
            "name": obj.item.product.name,
            "price": obj.item.price
        }
        return mydick
    def get_item_total(self,obj):
        return obj.item.price * obj.quantity

class CartDetailSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = [
            'id', 
            '__str__',
            'customer',
            'ordered',
            'discounted',
            'coupon',
            'total',
            'order_items'
            ]

    def get_order_items(self,obj):
        queryset            = OrderedItem.objects.filter(cart=obj.id)
        cartDetailSeri      = OrderedItemSerializer(queryset,many=True).data
        return cartDetailSeri

class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id', 
            '__str__',
            'customer',
            'ordered',
            'discounted',
            'coupon',
            'total',
            ]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id', 
            '__str__',
            'coupon',
            'discounted',
            'total',
            ]
    def is_valid(self, cart_id, code, user, raise_exception=False):
        try:
            cart                = Cart.objects.get(id=cart_id)
            queryset            = OrderedItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            return False

        cart                = Cart.objects.filter(id=cart_id)
        coupon              = get_object_or_404(Coupon,code=code)
        if coupon.customer is not None:
            if (user.id != coupon.customer.id):
                return False
        if coupon.coupon_type == '-1':
            return False
        elif coupon.coupon_type == '0' or coupon.coupon_type == '1':
            pass
        elif coupon.coupon_type == '2':
            if cart.total < coupon.above:
                return False
        elif coupon.coupon_type == '3':
            if cart.discounted < coupon.above:
                return False
        else:
            return False
        return super().is_valid(raise_exception=raise_exception)

    def update(self,cart_id):
        cart = Cart.objects.get(id=cart_id)
        print(self.validated_data['coupon'])
        if self.validated_data['coupon']:
            cart.coupon = self.validated_data['coupon']

        coupon = get_object_or_404(Coupon,code=cart.coupon)
        cart.discounted = cart.total
        if coupon.coupon_type == '0':
            cart.discounted -= cart.discounted/100*coupon.amount
        elif coupon.coupon_type == '1':
            cart.discounted -= coupon.amount
        elif coupon.coupon_type == '2':
            cart.discounted = cart.discounted/100*coupon.amount
        elif coupon.coupon_type == '3':
            cart.discounted -= coupon.amount
        cart.save()

