from rest_framework.permissions import BasePermission

class IsStore(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_store

    def has_permission(self,request):
        return request.user.is_store

class IsDelivery(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_delivery

    def has_permission(self,request):
        return request.user.is_delivery

class IsBurhan(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_burhan

    def has_permission(self,request):
        return request.user.is_burhan

class IsEditor(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_editor

    def has_permission(self,request):
        return request.user.is_editor

class IsStaff(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_staff

    def has_permission(self,request):
        return request.user.is_staff

class IsAccounting(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_accounting

    def has_permission(self,request):
        return request.user.is_accounting

class IsCustomerService(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_customerservice

    def has_permission(self,request):
        return request.user.is_customerservice

class IsBakery(BasePermission):
    message = "You do not have a permission to make this request." 
    def has_object_permission(self,request,view,obj):
        return request.user.is_bakery

    def has_permission(self,request):
        return request.user.is_bakery

