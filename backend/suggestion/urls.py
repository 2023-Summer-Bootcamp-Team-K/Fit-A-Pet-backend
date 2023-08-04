from django.urls import path
from .views import *

app_name = 'suggestion'

urlpatterns = [
    path('<int:user_id>/', SuggestionView.as_view(), name='suggestions'),
]