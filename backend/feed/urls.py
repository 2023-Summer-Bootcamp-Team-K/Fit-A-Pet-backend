from django.urls import path

from feed.views import FeedRecommendAPIView

app_name = 'feed'

urlpatterns = [
    path('<int:pk>/', FeedRecommendAPIView.as_view(), name='feed-recommend')
]