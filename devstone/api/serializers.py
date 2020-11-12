from rest_framework import serializers
from accounts.models import Cart,Order
from rest_auth.serializers import UserDetailsSerializer

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

class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id', 
            'customer',
            'ordered',
            'total',
            ]