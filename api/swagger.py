"""
Configuration Swagger pour GeoHeritage API
Documentation automatique des endpoints JWT
"""

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view, spec_validator

class SwaggerSchema:
    """
    Schéma Swagger personnalisé pour GeoHeritage
    """
    info = {
        'title': 'GeoHeritage API',
        'description': 'API REST pour la gestion des patrimoines culturels',
        'version': '1.0.0',
        'contact': {
            'name': 'GeoHeritage Team',
            'email': 'contact@geoheritage.com',
        },
    }
    
    servers = [
        {
            'url': 'http://127.0.0.1:8000/api/',
            'description': 'Serveur de développement',
        },
    ]
    
    security_schemes = [
        {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
            'description': 'Token JWT pour l\'authentification',
        }
    ]


swagger_config = {
    'title': 'GeoHeritage API Documentation',
    'url': '/api/docs/',
    'description': 'Documentation interactive de l\'API GeoHeritage',
    'auth': ['bearer'],
    'permission_classes': [permissions.AllowAny],
    'patterns': [
        {
            'url': r'^api/',
            'namespace': 'api',
        }
    ],
}

schema_view = get_schema_view(
    openapi.Info(
        title=swagger_config['title'],
        default_version='v1',
        description=swagger_config['description'],
        terms_of_service="https://www.geoheritage.com/terms/",
        contact=openapi.Contact(email="contact@geoheritage.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=swagger_config['permission_classes'],
    patterns=swagger_config['patterns']
)
