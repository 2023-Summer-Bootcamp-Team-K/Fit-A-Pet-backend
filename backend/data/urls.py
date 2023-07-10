from django.urls import path

from . import views

urlpatterns = [
    path('<int:pet_id>/', views.get_data),
    path('one-day/<int:pet_id>/', views.get_one_day_data),
    path('one-week/<int:pet_id>/', views.get_one_week_data),
    path('one-month/<int:pet_id>/', views.get_one_month_data),
]
