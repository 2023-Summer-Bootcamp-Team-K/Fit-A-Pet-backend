from django.urls import path

from . import views
from .views import start_scheduler

urlpatterns = [
    path('<int:pet_id>/', views.get_data),
    path('one-day/<int:pet_id>/', views.get_one_day_data),
    path('one-week/<int:pet_id>/', views.get_one_week_data),
    path('one-month/<int:pet_id>/', views.get_one_month_data),
    path('scheduler/<int:user_id>/', start_scheduler, name='start-scheduler'),
    path('hba1c/', views.calculate_hba1c),
]
