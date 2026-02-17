"""
Permissions JWT pour GeoHeritage API
Basées sur les rôles et niveaux hérités du système existant
"""

from rest_framework.permissions import BasePermission
from django.db import models


class IsAdminUser(BasePermission):
    """
    Permission pour les administrateurs (level 1)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Vérifier si l'utilisateur a le niveau admin (level 1)
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        return user_level <= 1


class IsModeratorUser(BasePermission):
    """
    Permission pour les modérateurs et administrateurs (level 2+)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        return user_level <= 2


class IsContributorUser(BasePermission):
    """
    Permission pour les contributeurs, modérateurs et administrateurs (level 3+)
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        return user_level <= 3


class IsAuthenticatedUser(BasePermission):
    """
    Permission pour tous les utilisateurs authentifiés (level 4+)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated


class CanCreatePatrimoine(BasePermission):
    """
    Permission pour créer un patrimoine (contributeur+)
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        return user_level <= 3


class CanEditPatrimoine(BasePermission):
    """
    Permission pour modifier un patrimoine
    - Admin/Modérateur : tous les patrimoines
    - Contributeur : uniquement ses patrimoines
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        
        # Admin et modérateur peuvent tout modifier
        if user_level <= 2:
            return True
        
        # Contributeur peut modifier uniquement ses patrimoines
        if user_level == 3 and hasattr(obj, 'created_by') and obj.created_by == request.user:
            return True
        
        return False


class CanDeletePatrimoine(BasePermission):
    """
    Permission pour supprimer un patrimoine
    - Admin/Modérateur : tous les patrimoines
    - Contributeur : uniquement ses patrimoines
    """
    def has_object_permission(self, request, view, obj):
        # Même logique que l'édition
        return CanEditPatrimoine().has_object_permission(request, view, obj)


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission en lecture seule sauf pour le propriétaire
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Lecture seule pour tout le monde
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Écriture seule pour le propriétaire ou admin/modérateur
        user_level = request.user.roles.aggregate(models.Min('level'))['level__min'] or 999
        if user_level <= 2:
            return True
        
        return hasattr(obj, 'created_by') and obj.created_by == request.user
