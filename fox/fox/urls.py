from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static

from fox import settings
from advertisement import views

def trigger_error(request):
	division_by_zero = 1 / 0	# for testing sentry monitoring

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('change_password', views.change_password, name='change_password'),
    path('advertisement/', include('advertisement.urls')),
    path('admin/', admin.site.urls),
	path('sentry-debug/', trigger_error), 	# for testing sentry monitoring
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
