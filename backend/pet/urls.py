from django.urls import path
from .views import *

app_name = 'pet'

urlpatterns = [
    path('create/<int:user_id>/', PetCreateView.as_view(), name='pet_create'),
    path('modify/<int:pet_id>/', PetModifyView.as_view(), name='pet_modify'),
    path('delete/<int:pet_id>/', PetDeleteView.as_view(), name='pet_delete'),
    path('detail/<int:pet_id>/', PetDetailView.as_view(), name='pet_detail'),
    path('list/<int:user_id>/', PetListView.as_view(), name='pet_list')
]