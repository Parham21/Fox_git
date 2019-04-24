from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static

from fox import settings
from advertisement import views

urlpatterns = [
    path('', views.home),
    path('login', views.login_view),
    path('register', views.register),
    path('reset_password', views.reset_password),
    path('advertisement/', include('advertisement.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)