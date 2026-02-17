"""
Serializers JWT pour GeoHeritage API
Conversion des modèles Django en format JSON pour l'API REST
"""

from rest_framework import serializers
from heritage.models import Patrimoine
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour les utilisateurs avec rôles
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'roles']
        read_only_fields = ['id']


class PatrimoineSerializer(serializers.ModelSerializer):
    """
    Serializer pour les patrimoines
    """
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Patrimoine
        fields = [
            'id', 'nom', 'description', 'type', 'latitude', 'longitude',
            'ville', 'date_creation', 'photo_url', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatrimoineCreateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la création de patrimoines
    """
    class Meta:
        model = Patrimoine
        fields = [
            'nom', 'description', 'type', 'latitude', 'longitude',
            'ville', 'date_creation', 'photo_url'
        ]


class PatrimoineUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer pour la mise à jour des patrimoines
    """
    class Meta:
        model = Patrimoine
        fields = [
            'nom', 'description', 'type', 'latitude', 'longitude',
            'ville', 'date_creation', 'photo_url'
        ]
        read_only_fields = ['id', 'created_by']


class PatrimoineMapSerializer(serializers.ModelSerializer):
    """
    Serializer léger pour les cartes Angular
    """
    popup_content = serializers.SerializerMethodField()
    
    class Meta:
        model = Patrimoine
        fields = [
            'id', 'nom', 'latitude', 'longitude', 'type', 
            'ville', 'photo_url', 'popup_content'
        ]
    
    def get_popup_content(self, obj):
        return f"<strong>{obj.nom}</strong><br>{obj.ville}<br>{obj.type}"


class TokenSerializer(serializers.Serializer):
    """
    Serializer pour les tokens JWT
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    def create(self, validated_data):
        # Personnaliser la réponse du token
        return {
            'access': validated_data.get('access'),
            'refresh': validated_data.get('refresh'),
            'token_type': 'Bearer',
            'expires_in': 3600,  # 1 heure en secondes
        }
