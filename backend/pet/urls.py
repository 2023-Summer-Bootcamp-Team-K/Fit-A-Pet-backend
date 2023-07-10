from django.urls import path
from .views import PetCreateAPIView

app_name = 'pet'

urlpatterns = [
    path('create/', PetCreateAPIView.as_view(), name='pet_create'),
]