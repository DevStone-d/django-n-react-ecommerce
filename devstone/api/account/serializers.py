from rest_framework import serializers
from accounts.models import Account,OrderedItem
from rest_auth.serializers import UserDetailsSerializer

class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = [
            'id', 
            'cart', 
            'item',
            'quantity',
            ]

class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name',
            'phone',
            'date_of_birth',
            'gender',
            ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'first_name', 
            'last_name',
            'phone',
            'date_of_birth',
            'gender',
            ]

    def update(self,usermail):
        account = Account.objects.get(email=usermail)
        
        if self.validated_data['first_name']:
            account.first_name = self.validated_data['first_name']

        if self.validated_data['last_name']:
            account.last_name = self.validated_data['last_name']

        if self.validated_data['phone']:
            account.phone = self.validated_data['phone']
        
        if self.validated_data['date_of_birth']:
            account.date_of_birth = self.validated_data['date_of_birth']
        
        if self.validated_data['gender']:
            account.gender = self.validated_data['gender']
        
        account.save()

        return account
