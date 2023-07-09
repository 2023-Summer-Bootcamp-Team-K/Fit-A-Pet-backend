from django.urls import path

from . import views

app_name = 'pet'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.pet_create, name='pet_create'),
]