from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Fit-A-Pet",
        default_version='v1',
        description="반려동물을 위한 맞춤 사료 추천",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # django
    path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
    path('api/feeds/', include('feed.urls')),
    path('api/pets/', include('pet.urls')),
    path('api/data/', include('data.urls')),
]
