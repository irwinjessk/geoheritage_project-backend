"""
Tests JWT pour GeoHeritage API
Validation complète de l'authentification et des permissions
"""

from .test_jwt_auth import JWTAuthenticationTestCase

__all__ = [
    'JWTAuthenticationTestCase',
]