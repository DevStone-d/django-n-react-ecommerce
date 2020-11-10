from django.contrib import admin
from accounts.models import Account,Adress,Cart,OrderedItem
# Register your models here.

admin.site.register(Account)
admin.site.register(Adress)
admin.site.register(Cart)
admin.site.register(OrderedItem)