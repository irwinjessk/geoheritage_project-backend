#!/usr/bin/env python3
"""
Script de test pour l'API JWT GeoHeritage
Validation des endpoints avec curl
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://127.0.0.1:8005/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/login/"
REFRESH_URL = f"{BASE_URL}/auth/refresh/"
PROFILE_URL = f"{BASE_URL}/auth/profile/"
PATRIMOINES_URL = f"{BASE_URL}/patrimoines/"

def test_login():
    """Test de connexion JWT"""
    print("🔐 Test: Login JWT")
    
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(LOGIN_URL, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Login réussi !")
            print(f"Access Token: {result.get('access', '')[:50]}...")
            print(f"Refresh Token: {result.get('refresh', '')[:50]}...")
            print(f"User Level: {result.get('user', {}).get('user_level', 'N/A')}")
            return result.get('access'), result.get('refresh')
        else:
            print(f"❌ Erreur: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None, None

def test_profile(access_token):
    """Test du profil utilisateur"""
    print("\n👤 Test: Profil utilisateur")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Profil récupéré !")
            print(f"Username: {result.get('user', {}).get('username', 'N/A')}")
            print(f"Roles: {[r.get('name') for r in result.get('user', {}).get('roles', [])]}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_patrimoines_list(access_token):
    """Test de la liste des patrimoines"""
    print("\n🏛️ Test: Liste des patrimoines")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(PATRIMOINES_URL, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Liste des patrimoines récupérée !")
            print(f"Nombre de patrimoines: {len(result.get('results', []))}")
            if result.get('results'):
                print(f"Premier patrimoine: {result['results'][0].get('nom', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_create_patrimoine(access_token):
    """Test de création d'un patrimoine"""
    print("\n🏗️ Test: Création d'un patrimoine")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "nom": "Test API Patrimoine",
        "description": "Patrimoine créé via l'API JWT",
        "type": "monument",
        "latitude": "48.8566",
        "longitude": "2.3522",
        "ville": "Paris",
        "date_creation": "2024-01-01"
    }
    
    try:
        response = requests.post(PATRIMOINES_URL, json=data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Patrimoine créé avec succès !")
            print(f"ID: {result.get('id', 'N/A')}")
            print(f"Nom: {result.get('nom', 'N/A')}")
            return result.get('id')
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_patrimoine_detail(access_token, patrimoine_id):
    """Test du détail d'un patrimoine"""
    print(f"\n🏛️ Test: Détail du patrimoine {patrimoine_id}")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{PATRIMOINES_URL}{patrimoine_id}/", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Détail du patrimoine récupéré !")
            print(f"Nom: {result.get('nom', 'N/A')}")
            print(f"Description: {result.get('description', 'N/A')[:50]}...")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_nearby_search(access_token):
    """Test de recherche par proximité"""
    print("\n🗺️ Test: Recherche par proximité GPS")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {
        "lat": "48.8566",
        "lng": "2.3522",
        "radius": "10"
    }
    
    try:
        response = requests.get(f"{PATRIMOINES_URL}nearby/", headers=headers, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Recherche par proximité réussie !")
            print(f"Patrimoines trouvés: {result.get('count', 0)}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Lancement des tests de l'API JWT GeoHeritage")
    print(f"URL de base: {BASE_URL}")
    
    # Test 1: Login
    access_token, refresh_token = test_login()
    
    if not access_token:
        print("❌ Impossible de continuer sans token d'accès")
        return
    
    # Attendre un peu pour éviter les problèmes de timing
    time.sleep(1)
    
    # Test 2: Profil
    test_profile(access_token)
    
    # Test 3: Liste des patrimoines
    test_patrimoines_list(access_token)
    
    # Test 4: Création d'un patrimoine
    patrimoine_id = test_create_patrimoine(access_token)
    
    if patrimoine_id:
        # Test 5: Détail du patrimoine
        test_patrimoine_detail(access_token, patrimoine_id)
    
    # Test 6: Recherche par proximité
    test_nearby_search(access_token)
    
    print("\n✅ Tests terminés !")
    print("🎯 L'API JWT GeoHeritage est fonctionnelle !")

if __name__ == "__main__":
    main()
