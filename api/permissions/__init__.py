"""
Permissions JWT pour GeoHeritage API
Gestion des permissions basées sur les rôles avec JWT
"""

from django.db import models
from rest_framework.permissions import BasePermission

from .permissions import (
    IsAdminUser,
    IsModeratorUser,
    IsContributorUser,
    IsAuthenticatedUser,
    CanCreatePatrimoine,
    CanEditPatrimoine,
    CanDeletePatrimoine,
    IsOwnerOrReadOnly,
)

__all__ = [
    'IsAdminUser',
    'IsModeratorUser', 
    'IsContributorUser',
    'IsAuthenticatedUser',
    'CanCreatePatrimoine',
    'CanEditPatrimoine',
    'CanDeletePatrimoine',
    'IsOwnerOrReadOnly',
]