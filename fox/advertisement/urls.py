from django.urls import path

from . import views

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('search', views.search, name='search'),
    path('favorites_advertisement', views.favorite_advertisement, name='favorite_advertisement'),
    path('add_advertisement', views.add_advertisement, name='add_advertisement'),
    path('<int:advertisement_id>/', views.advertisement_detail, name='advertisement_detail')
]