from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('advertisement/', include('advertisement.urls')),
    path('admin/', admin.site.urls),
]
