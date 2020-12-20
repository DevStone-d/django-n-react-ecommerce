from django.contrib import admin

# Register your models here.
from core.models import SiteMapItem,Categories


admin.site.register(SiteMapItem)
# admin.site.register(SiteMap)

admin.site.register(Categories)