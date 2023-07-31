from django.urls import path

from . import views

urlpatterns = [
    path('hba1c/<int:pet_id>/', views.calculate_hba1c, name='calculate-hba1c'),
    path('recent/<int:pet_id>/', views.get_most_recent_data, name='get-most-recent-data'),
    path('<int:month>-<int:day>/<int:pet_id>/', views.get_one_day_data),
    path('<int:start_month>-<int:start_day>/<int:end_month>-<int:end_day>/<int:pet_id>/', views.get_interval_data),
    path('<int:month>/<int:pet_id>/', views.get_month_data),
]