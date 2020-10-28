from django.contrib import admin


from products.models import Collection,Product,ProductDetail,ProductMedia,Tag
# Register your models here.


admin.site.register(Collection)
admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(ProductMedia)
admin.site.register(Tag)
