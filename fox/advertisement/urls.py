from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('search', views.search, name='search'),
    path('adv_search', views.adv_search, name='adv_search'),
    path('favorites_advertisement', views.favorite_advertisement, name='favorite_advertisement'),
    path('add_advertisement', views.add_advertisement, name='add_advertisement'),
    path('profile', views.profile, name='profile'),
    path('my_advertisements', views.my_advertisements, name='my_advertisements'),
    path('<int:advertisement_id>/', views.advertisement_detail, name='advertisement_detail'),
    path('<int:advertisement_id>/add_favorite_advertisement', views.add_favorite_advertisement,
         name='add_favorite_advertisement'),
    path('<int:advertisement_id>/report_advertisement', views.report_advertisement,
         name='report_advertisement')

]
