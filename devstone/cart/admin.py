from django.contrib import admin
from .models import Cart,OrderedItem,Order

admin.site.register(Cart)
admin.site.register(OrderedItem)
admin.site.register(Order)
