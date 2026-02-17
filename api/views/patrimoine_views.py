"""
Vues JWT pour les patrimoines GeoHeritage
CRUD operations avec permissions JWT
"""

from rest_framework import status, generics, filters, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from heritage.models import Patrimoine
from api.permissions import (
    IsAdminUser, IsModeratorUser, IsContributorUser,
    CanCreatePatrimoine, CanEditPatrimoine, CanDeletePatrimoine
)
from api.serializers import (
    PatrimoineSerializer, PatrimoineCreateSerializer,
    PatrimoineUpdateSerializer, PatrimoineMapSerializer
)


class PatrimoinePagination(PageNumberPagination):
    """
    Pagination personnalisée pour les patrimoines
    """
    page_size = 12
    page_size_query_param = 'page'
    max_page_size = 100


class PatrimoineListCreateView(generics.ListCreateAPIView):
    """
    Vue pour lister et créer des patrimoines
    """
    permission_classes = [CanCreatePatrimoine]
    serializer_class = PatrimoineSerializer
    pagination_class = PatrimoinePagination
    queryset = Patrimoine.objects.all()
    
    def get_queryset(self):
        queryset = Patrimoine.objects.all()
        
        # Filtre par ville
        ville = self.request.query_params.get('ville')
        if ville:
            queryset = queryset.filter(ville__icontains=ville)
        
        # Filtre par type
        type_site = self.request.query_params.get('type')
        if type_site:
            queryset = queryset.filter(type__icontains=type_site)
        
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatrimoineCreateSerializer
        return PatrimoineSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatrimoineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vue pour détail, mise à jour et suppression d'un patrimoine
    """
    queryset = Patrimoine.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]  # Lecture pour tous les authentifiés
        elif self.request.method in ['PUT', 'PATCH']:
            return [CanEditPatrimoine()]  # Modification selon permissions
        elif self.request.method == 'DELETE':
            return [CanDeletePatrimoine()]  # Suppression selon permissions
        return []
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PatrimoineUpdateSerializer
        return PatrimoineSerializer


class PatrimoineNearbyView(views.APIView):
    """
    Vue pour la recherche par proximité GPS
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        radius = request.GET.get('radius', 10)  # 10km par défaut
        
        if not lat or not lng:
            return Response({
                'error': 'Coordonnées GPS requises',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
        except ValueError:
            return Response({
                'error': 'Coordonnées invalides',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Implémentation de la recherche par proximité (Haversine)
        from math import radians, sin, cos, sqrt, atan2
        
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Rayon de la Terre en km
            lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c  # Distance en km
            return distance
        
        patrimoines = Patrimoine.objects.all()
        nearby_patrimoines = []
        
        for patrimoine in patrimoines:
            if patrimoine.latitude and patrimoine.longitude:
                distance = calculate_distance(
                    lat, lng,
                    float(patrimoine.latitude), float(patrimoine.longitude)
                )
                if distance <= radius:  # Distance déjà en km
                    patrimoine.distance_km = distance
                    nearby_patrimoines.append(patrimoine)
        
        # Trier par distance
        nearby_patrimoines.sort(key=lambda p: p.distance_km)
        
        serializer = PatrimoineSerializer(nearby_patrimoines, many=True)
        
        return Response({
            'patrimoines': serializer.data,
            'count': len(nearby_patrimoines),
            'search_params': {
                'latitude': float(lat),
                'longitude': float(lng),
                'radius_km': float(radius)
            }
        })


class PatrimoineMapView(views.APIView):
    """
    Endpoint optimisé pour Angular - données légères pour la carte
    """
    permission_classes = []  # Accès public pour la carte
    
    def get(self, request):
        patrimoines = Patrimoine.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
        
        serializer = PatrimoineMapSerializer(patrimoines, many=True)
        
        return Response({
            'sites': serializer.data,
            'count': len(patrimoines),
            'last_updated': patrimoines.order_by('-updated_at').first().updated_at if patrimoines else None
        })
