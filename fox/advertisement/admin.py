from django.contrib import admin

from .models import Advertiser, Advertisement, City, Area, Category

admin.site.register(Advertiser)
admin.site.register(Advertisement)
admin.site.register(City)
admin.site.register(Area)
admin.site.register(Category)

