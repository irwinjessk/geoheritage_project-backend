"""
Vues JWT pour l'authentification GeoHeritage
Login, logout, refresh tokens avec JWT
"""

from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from django.db import models
from api.serializers import TokenSerializer
from api.permissions import IsAdminUser


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour obtenir les tokens JWT
    """
    def post(self, request, *args, **kwargs):
        # Surcharge pour ajouter les informations utilisateur dans la réponse
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Récupérer l'utilisateur authentifié depuis le token
            from rest_framework_simplejwt.tokens import AccessToken
            access_token = AccessToken(response.data['access'])
            user_id = access_token['user_id']
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=user_id)
            
            response.data.update({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'roles': [
                        {
                            'id': role.id,
                            'name': role.name,
                            'description': role.description,
                            'level': role.level
                        } for role in user.roles.all()
                    ],
                    'user_level': user.roles.aggregate(models.Min('level'))['level__min'] or 999
                },
                'permissions': {
                    'can_create_patrimoine': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 3,
                    'can_edit_all_patrimoines': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 2,
                    'can_delete_all_patrimoines': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 2,
                }
            })
        
        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Vue personnalisée pour rafraîchir le token JWT
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            response.data.update({
                'message': 'Token rafraîchi avec succès',
                'token_type': 'Bearer'
            })
        
        return response


class LogoutView(views.APIView):
    """
    Vue pour la déconnexion (blacklist du token)
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Simple logout sans blacklist pour l'instant
                # Dans une vraie application, vous pourriez implémenter une blacklist
                pass
            
            return Response({
                'message': 'Déconnexion réussie',
                'status': 'success'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': 'Erreur lors de la déconnexion',
                'status': 'error',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(views.APIView):
    """
    Vue pour obtenir le profil utilisateur avec permissions
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': [
                    {
                        'id': role.id,
                        'name': role.name,
                        'description': role.description,
                        'level': role.level
                    } for role in user.roles.all()
                ],
                'user_level': user.roles.aggregate(models.Min('level'))['level__min'] or 999
            },
            'permissions': {
                'can_create_patrimoine': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 3,
                'can_edit_all_patrimoines': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 2,
                'can_delete_all_patrimoines': user.roles.aggregate(models.Min('level'))['level__min'] or 999 <= 2,
            }
        })
