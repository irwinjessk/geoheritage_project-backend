"""
Swagger configuration for GeoHeritage API
"""

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GeoHeritage API",
        default_version='v1',
        description="API for managing geographical and cultural heritage sites",
        terms_of_service="https://www.geoheritage.com/terms/",
        contact=openapi.Contact(email="contact@geoheritage.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
