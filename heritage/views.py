from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from account.decorators import can_edit_patrimoine, contributeur_required, get_user_level
from .models import Patrimoine
from account.models import User


def patrimoine_list(request):
    """Liste des patrimoines (accessible à tous)"""
    patrimoines = Patrimoine.objects.all()
    
    # Filtres
    ville = request.GET.get('ville')
    type_patrimoine = request.GET.get('type')
    
    if ville:
        patrimoines = patrimoines.filter(ville__icontains=ville)
    if type_patrimoine:
        patrimoines = patrimoines.filter(type=type_patrimoine)
    
    context = {
        'patrimoines': patrimoines,
        'villes': Patrimoine.objects.values_list('ville', flat=True).distinct(),
        'types': Patrimoine.TYPE_CHOICES,
    }
    return render(request, 'heritage/list.html', context)


def patrimoine_detail(request, pk):
    """Détail d'un patrimoine"""
    patrimoine = get_object_or_404(Patrimoine, pk=pk)
    return render(request, 'heritage/detail.html', {'patrimoine': patrimoine})


@login_required
def patrimoine_create(request):
    """Créer un patrimoine (utilisateur connecté)"""
    print(f"DEBUG: User {request.user.username} est connecté et essaie de créer un patrimoine")
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        type_patrimoine = request.POST.get('type')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        ville = request.POST.get('ville')
        date_creation = request.POST.get('date_creation')
        photo_url = request.POST.get('photo_url')
        
        patrimoine = Patrimoine.objects.create(
            nom=nom,
            description=description,
            type=type_patrimoine,
            latitude=latitude,
            longitude=longitude,
            ville=ville,
            date_creation=date_creation,
            photo_url=photo_url if photo_url else None,
            created_by=request.user
        )
        
        messages.success(request, f'Patrimoine "{patrimoine.nom}" créé avec succès')
        return redirect('heritage:detail', pk=patrimoine.pk)
    
    return render(request, 'heritage/create.html', {'types': Patrimoine.TYPE_CHOICES})


@login_required
def patrimoine_update(request, pk):
    """Modifier un patrimoine (utilisateur connecté)"""
    patrimoine = get_object_or_404(Patrimoine, pk=pk)
    
    if request.method == 'POST':
        patrimoine.nom = request.POST.get('nom', patrimoine.nom)
        patrimoine.description = request.POST.get('description', patrimoine.description)
        patrimoine.type = request.POST.get('type', patrimoine.type)
        patrimoine.latitude = request.POST.get('latitude', patrimoine.latitude)
        patrimoine.longitude = request.POST.get('longitude', patrimoine.longitude)
        patrimoine.ville = request.POST.get('ville', patrimoine.ville)
        patrimoine.date_creation = request.POST.get('date_creation', patrimoine.date_creation)
        patrimoine.photo_url = request.POST.get('photo_url', patrimoine.photo_url)
        patrimoine.save()
        
        messages.success(request, f'Patrimoine "{patrimoine.nom}" mis à jour')
        return redirect('heritage:detail', pk=patrimoine.pk)
    
    return render(request, 'heritage/update.html', {
        'patrimoine': patrimoine,
        'types': Patrimoine.TYPE_CHOICES
    })


@login_required
def patrimoine_delete(request, pk):
    """Supprimer un patrimoine (utilisateur connecté)"""
    patrimoine = get_object_or_404(Patrimoine, pk=pk)
    
    if request.method == 'POST':
        nom = patrimoine.nom
        patrimoine.delete()
        messages.success(request, f'Patrimoine "{nom}" supprimé avec succès')
        return redirect('heritage:list')
    
    return render(request, 'heritage/delete.html', {'patrimoine': patrimoine})


def patrimoine_search(request):
    """Recherche de patrimoines"""
    query = request.GET.get('q')
    patrimoines = Patrimoine.objects.all()
    
    if query:
        patrimoines = patrimoines.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(ville__icontains=query)
        )
    
    return render(request, 'heritage/search.html', {
        'patrimoines': patrimoines,
        'query': query
    })


def patrimoine_map(request):
    """
    Vue pour afficher la carte des patrimoines
    """
    patrimoines = Patrimoine.objects.all()
    
    # Préparer les données pour la carte
    sites_data = []
    for patrimoine in patrimoines:
        sites_data.append({
            'id': patrimoine.pk,
            'nom': patrimoine.nom,
            'description': patrimoine.description[:100] + '...' if len(patrimoine.description) > 100 else patrimoine.description,
            'type': patrimoine.type,
            'lat': float(patrimoine.latitude),
            'lng': float(patrimoine.longitude),
            'ville': patrimoine.ville,
            'url': reverse('heritage:detail', args=[patrimoine.pk]),
            'photo_url': patrimoine.photo_url
        })
    
    return render(request, 'heritage/map.html', {
        'sites': json.dumps(sites_data),
        'sites_count': len(sites_data)
    })


def patrimoine_nearby(request):
    """Recherche de patrimoines par proximité GPS"""
    import math
    import json
    
    # Récupérer les paramètres
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius', 10)  # Rayon par défaut: 10km
    
    patrimoines = Patrimoine.objects.all()
    
    if lat and lng:
        try:
            lat = float(lat)
            lng = float(lng)
            radius = float(radius)
            
            # Calculer la distance pour chaque patrimoine (formule Haversine)
            patrimoines_with_distance = []
            for patrimoine in patrimoines:
                distance = calculate_distance(lat, lng, patrimoine.latitude, patrimoine.longitude)
                if distance <= radius:
                    patrimoine.distance = distance
                    patrimoines_with_distance.append(patrimoine)
            
            # Trier par distance
            patrimoines_with_distance.sort(key=lambda p: p.distance)
            patrimoines = patrimoines_with_distance
            
            message = f"{len(patrimoines)} site(s) trouvé(s) dans un rayon de {radius}km"
            
        except ValueError:
            message = "Coordonnées GPS invalides"
    else:
        message = "Veuillez spécifier des coordonnées GPS pour la recherche"
    
    return render(request, 'heritage/nearby.html', {
        'patrimoines': json.dumps([
            {
                'id': p.pk,
                'nom': p.nom,
                'ville': p.ville,
                'type': p.get_type_display(),
                'latitude': float(p.latitude),
                'longitude': float(p.longitude),
                'distance': float(p.distance) if hasattr(p, 'distance') else 0
            } for p in patrimoines
        ]),
        'patrimoines_list': patrimoines,  # Pour le template HTML
        'message': message,
        'center_lat': lat or 48.8566,  # Paris par défaut
        'center_lng': lng or 2.3522,
        'zoom': 12 if lat and lng else 6
    })


def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculer la distance entre deux points GPS (formule Haversine)"""
    import math
    
    # Rayon de la Terre en km
    R = 6371
    
    # Conversion en radians
    lat1_rad = math.radians(lat1)
    lng1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lng2_rad = math.radians(lng2)
    
    # Différences
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Formule Haversine
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Distance en km
    distance = R * c
    
    return round(distance, 2)
