from django.urls import path

from . import views
from .views import start_scheduler

urlpatterns = [
    path('<int:pet_id>/', views.get_data),
    path('one-day/<int:pet_id>/', views.get_one_day_data),
    path('one-week/<int:pet_id>/', views.get_one_week_data),
    path('one-month/<int:pet_id>/', views.get_one_month_data),
    path('scheduler/<int:user_id>/', start_scheduler, name='start-scheduler'),
    path('hba1c/<int:pet_id>/', views.calculate_hba1c),
    path('recent/<int:pet_id>/', views.get_most_recent_data),
    path('<int:month>-<int:day>/<int:pet_id>/', views.get_one_day_data),
    path('<int:start_month>-<int:start_day>/<int:end_month>-<int:end_day>/<int:pet_id>/', views.get_interval_data),
    path('<int:month>/<int:pet_id>/', views.get_month_data),
]