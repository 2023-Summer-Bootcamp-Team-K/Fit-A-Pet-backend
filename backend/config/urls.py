from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Fit-A-Pet",
        default_version='v1',
        description="반려동물을 위한 맞춤 사료 추천",
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # swagger
    path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),

    # django
    path('admin/', admin.site.urls),
    path('api/pets/', include('pet.urls')),
]