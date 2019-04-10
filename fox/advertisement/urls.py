from django.urls import path

from . import views

urlpatterns = [
    path('search', views.search, name='search'),
    path('add_advertisement', views.add_advertisement, name='add_advertisement')
]