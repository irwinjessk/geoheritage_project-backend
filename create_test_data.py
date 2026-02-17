#!/usr/bin/env python3
"""
Script pour créer des données de test réelles de patrimoine français
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from heritage.models import Patrimoine
from account.models import User

def create_test_patrimoines():
    """Créer des sites patrimoniaux français réels"""
    
    # Récupérer l'utilisateur admin
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("❌ Utilisateur admin non trouvé. Créez d'abord un utilisateur admin.")
        return
    
    # Données de sites patrimoniaux réels
    sites_patrimoniaux = [
        {
            "nom": "Tour Eiffel",
            "description": "Tour en fer puddlé de 324 mètres de hauteur construite par Gustave Eiffel pour l'Exposition universelle de 1889. Devenue le symbole de Paris et de la France.",
            "type": "monument",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "ville": "Paris",
            "date_creation": "1889-03-31",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons.jpg/800px-Tour_Eiffel_Wikimedia_Commons.jpg"
        },
        {
            "nom": "Cathédrale Notre-Dame de Paris",
            "description": "Chef-d'œuvre de l'architecture gothique française, construite entre 1163 et 1345. Située sur l'île de la Cité, elle est l'un des monuments les plus visités de Paris.",
            "type": "monument",
            "latitude": 48.8530,
            "longitude": 2.3499,
            "ville": "Paris",
            "date_creation": "1345-12-01",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Notre_Dame_de_Paris_2013-06-15.jpg/800px-Notre_Dame_de_Paris_2013-06-15.jpg"
        },
        {
            "nom": "Musée du Louvre",
            "description": "Plus grand musée du monde et le plus visité, abritant des œuvres comme la Joconde et la Vénus de Milo. Installé dans le palais du Louvre, ancienne résidence royale.",
            "type": "musée",
            "latitude": 48.8606,
            "longitude": 2.3376,
            "ville": "Paris",
            "date_creation": "1793-08-10",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Louvre_Museum_Richard_Flaherty.jpg/800px-Louvre_Museum_Richard_Flaherty.jpg"
        },
        {
            "nom": "Arc de Triomphe",
            "description": "Monument érigé en l'honneur des victoires françaises et des soldats qui sont morts pour la France. Situé sur l'avenue des Champs-Élysées, il mesure 50 mètres de hauteur.",
            "type": "monument",
            "latitude": 48.8738,
            "longitude": 2.2950,
            "ville": "Paris",
            "date_creation": "1836-07-29",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Arc_de_Triomphe_1900.jpg/800px-Arc_de_Triomphe_1900.jpg"
        },
        {
            "nom": "Basilique du Sacré-Cœur",
            "description": "Basilique catholique située au sommet de la butte Montmartre. Style architectural romano-byzantin avec son dôme impressionnant, elle offre une vue panoramique sur Paris.",
            "type": "monument",
            "latitude": 48.8867,
            "longitude": 2.3431,
            "ville": "Paris",
            "date_creation": "1914-10-16",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Sacre-Coeur_Basilica_in_Paris.jpg/800px-Sacre-Coeur_Basilica_in_Paris.jpg"
        },
        {
            "nom": "Château de Versailles",
            "description": "Ancienne résidence royale et château monumental situé à Versailles. Classé au patrimoine mondial de l'UNESCO, il symbolise la monarchie absolue française.",
            "type": "bâtiment historique",
            "latitude": 48.8049,
            "longitude": 2.1204,
            "ville": "Versailles",
            "date_creation": "1682-05-06",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Palace_of_Versailles_aerial_view.jpg/800px-Palace_of_Versailles_aerial_view.jpg"
        },
        {
            "nom": "Mont-Saint-Michel",
            "description": "Commune insulaire normande et site touristique emblématique. L'abbaye bénédictine et son village médiéval forment un ensemble architectural exceptionnel.",
            "type": "site naturel",
            "latitude": 48.6360,
            "longitude": -1.5114,
            "ville": "Le Mont-Saint-Michel",
            "date_creation": "1023-10-10",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Mont_Saint-Michel_2013.jpg/800px-Mont_Saint-Michel_2013.jpg"
        },
        {
            "nom": "Pont du Gard",
            "description": "Aqueduc romain spectaculaire à trois niveaux, chef-d'œuvre de l'ingénierie antique. Classé au patrimoine mondial de l'UNESCO, il traverse le Gardon près de Nîmes.",
            "type": "monument",
            "latitude": 43.9472,
            "longitude": 4.5320,
            "ville": "Vers-Pont-du-Gard",
            "date_creation": "0019-01-01",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Pont_du_Gard_Oct_2006.jpg/800px-Pont_du_Gard_Oct_2006.jpg"
        },
        {
            "nom": "Cathédrale de Reims",
            "description": "Cathédrale gothique où les rois de France étaient couronnés. Connue pour ses sculptures exceptionnelles et ses vitraux, elle est classée au patrimoine mondial de l'UNESCO.",
            "type": "monument",
            "latitude": 49.2494,
            "longitude": 4.0347,
            "ville": "Reims",
            "date_creation": "1275-10-15",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Reims_Cathedral_2013-06-15.jpg/800px-Reims_Cathedral_2013-06-15.jpg"
        },
        {
            "nom": "Cité de Carcassonne",
            "description": "Forteresse médiévale remarquablement conservée avec ses 52 tours et son double enceinte. Site historique majeur du Languedoc, classé au patrimoine mondial de l'UNESCO.",
            "type": "bâtiment historique",
            "latitude": 43.2070,
            "longitude": 2.3500,
            "ville": "Carcassonne",
            "date_creation": "1150-12-31",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Cite_de_Carcassonne_vue_aerienne.jpg/800px-Cite_de_Carcassonne_vue_aerienne.jpg"
        },
        {
            "nom": "Gorges du Verdon",
            "description": "Canyon spectaculaire de l'Europe surnommé 'Grand Canyon du Verdon'. Parc naturel régional avec ses eaux turquoise et ses falaises calcaires impressionnantes.",
            "type": "site naturel",
            "latitude": 43.8480,
            "longitude": 6.2160,
            "ville": "Moustiers-Sainte-Marie",
            "date_creation": "1905-04-10",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Verdon_canyon_from_balcony_of_the_Martel_lookout.jpg/800px-Verdon_canyon_from_balcony_of_the_Martel_lookout.jpg"
        },
        {
            "nom": "Ménhirs de Carnac",
            "description": "Plus grand ensemble de mégalithes au monde avec plus de 3000 menhirs alignés sur près de 4 kilomètres. Site préhistorique majeur datant du Néolithique.",
            "type": "site archéologique",
            "latitude": 47.6098,
            "longitude": -3.0740,
            "ville": "Carnac",
            "date_creation": "1900-01-01",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Carnac_alignments_2007.jpg/800px-Carnac_alignments_2007.jpg"
        },
        {
            "nom": "Château de Chambord",
            "description": "Château de la Loire emblématique de la Renaissance française, construit pour François Ier. Célèbre pour son escalier double hélice et son architecture unique.",
            "type": "bâtiment historique",
            "latitude": 47.6165,
            "longitude": 1.5165,
            "ville": "Chambord",
            "date_creation": "1547-12-31",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Chateau_de_Chambord_2006.jpg/800px-Chateau_de_Chambord_2006.jpg"
        },
        {
            "nom": "Vieux Lyon",
            "description": "Quartier historique de Lyon avec ses traboules, ses immeubles de la Renaissance et ses restaurants traditionnels. Classé au patrimoine mondial de l'UNESCO.",
            "type": "bâtiment historique",
            "latitude": 45.7640,
            "longitude": 4.8357,
            "ville": "Lyon",
            "date_creation": "1450-12-31",
            "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Vieux_Lyon_vue_aerienne.jpg/800px-Vieux_Lyon_vue_aerienne.jpg"
        }
    ]
    
    print(f"🏗️ Création de {len(sites_patrimoniaux)} sites patrimoniaux réels...")
    
    created_count = 0
    for site_data in sites_patrimoniaux:
        # Vérifier si le site existe déjà
        existing_site = Patrimoine.objects.filter(nom=site_data['nom']).first()
        if existing_site:
            print(f"⚠️ {site_data['nom']} existe déjà, mise à jour...")
            existing_site.description = site_data['description']
            existing_site.type = site_data['type']
            existing_site.latitude = site_data['latitude']
            existing_site.longitude = site_data['longitude']
            existing_site.ville = site_data['ville']
            existing_site.date_creation = site_data['date_creation']
            existing_site.photo_url = site_data['photo_url']
            existing_site.save()
            created_count += 1
        else:
            # Créer le nouveau site
            site = Patrimoine.objects.create(
                nom=site_data['nom'],
                description=site_data['description'],
                type=site_data['type'],
                latitude=site_data['latitude'],
                longitude=site_data['longitude'],
                ville=site_data['ville'],
                date_creation=site_data['date_creation'],
                photo_url=site_data['photo_url'],
                created_by=admin_user
            )
            print(f"✅ {site_data['nom']} créé avec succès")
            created_count += 1
    
    print(f"\n🎉 {created_count} sites patrimoniaux créés/mis à jour avec succès !")
    
    # Statistiques
    total_sites = Patrimoine.objects.count()
    print(f"\n📊 Statistiques de la base de données :")
    print(f"   Total des sites : {total_sites}")
    
    # Par type
    types_count = Patrimoine.objects.values('type').distinct().count()
    print(f"   Types différents : {types_count}")
    
    # Par ville
    villes_count = Patrimoine.objects.values('ville').distinct().count()
    print(f"   Villes différentes : {villes_count}")
    
    # Distribution par type
    print(f"\n📍 Distribution par type :")
    for type_name in Patrimoine.objects.values_list('type', flat=True).distinct():
        count = Patrimoine.objects.filter(type=type_name).count()
        print(f"   {type_name}: {count} sites")

if __name__ == "__main__":
    create_test_patrimoines()
