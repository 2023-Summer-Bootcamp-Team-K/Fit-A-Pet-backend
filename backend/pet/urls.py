from django.urls import path
from .views import PetCreateView, PetModifyView, PetDeleteView, PetDetailView

app_name = 'pet'

urlpatterns = [
    path('create/', PetCreateView.as_view(), name='pet_create'),
    path('modify/<int:pet_id>/', PetModifyView.as_view(), name='pet_modify'),
    path('delete/<int:pet_id>/', PetDeleteView.as_view(), name='pet_delete'),
    path('detail/<int:pet_id>/', PetDetailView.as_view(), name='pet_detail'),
]