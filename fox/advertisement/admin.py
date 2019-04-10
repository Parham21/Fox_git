from django.contrib import admin

from .models import Advertiser, Advertisement, City, Area

admin.site.register(Advertiser)
admin.site.register(Advertisement)
admin.site.register(City)
admin.site.register(Area)

