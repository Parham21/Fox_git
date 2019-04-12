from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static

from fox import settings

urlpatterns = [
    path('advertisement/', include('advertisement.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)