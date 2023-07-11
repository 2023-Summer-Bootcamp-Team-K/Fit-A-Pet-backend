from django.urls import path

from . import views
from .views import start_scheduler

urlpatterns = [
    path('scheduler/<int:user_id>/', start_scheduler, name='start-scheduler')
]