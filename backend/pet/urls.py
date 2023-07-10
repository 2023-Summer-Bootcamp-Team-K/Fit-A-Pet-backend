from django.urls import path
from .views import PetCreateAPIView
from .views import PetModifyView

app_name = 'pet'

urlpatterns = [
    path('create/', PetCreateAPIView.as_view(), name='pet_create'),
    path('modify/<int:pet_id>/', PetModifyView.as_view(), name='pet_modify')
]