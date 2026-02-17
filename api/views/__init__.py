"""
Vues API GeoHeritage avec JWT
Authentification et gestion des patrimoines
"""

from .auth_views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
    UserProfileView,
)

from .patrimoine_views import (
    PatrimoineListCreateView,
    PatrimoineDetailView,
    PatrimoineNearbyView,
)

__all__ = [
    'CustomTokenObtainPairView',
    'CustomTokenRefreshView',
    'LogoutView',
    'UserProfileView',
    'PatrimoineListCreateView',
    'PatrimoineDetailView',
    'PatrimoineNearbyView',
]