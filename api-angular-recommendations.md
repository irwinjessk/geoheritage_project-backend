# API Optimisations pour Angular Frontend

## 🎯 Endpoints Recommandés pour Angular

### 1. **Carte et Marqueurs**
```http
GET /api/v1/patrimoines/map-data
```
**Retourne tous les sites avec coordonnées pour la carte**
```json
{
  "sites": [
    {
      "id": 1,
      "nom": "Tour Eiffel",
      "lat": 48.8584,
      "lng": 2.2945,
      "type": "monument",
      "ville": "Paris",
      "photo_url": "https://...",
      "popup_content": "Tour Eiffel - Paris"
    }
  ]
}
```

### 2. **Filtres Avancés**
```http
GET /api/v1/patrimoines/?ville=Paris&type=monument&page=1&page_size=20
```
**Pagination et filtres pour les listes**

### 3. **Recherche Proximité Améliorée**
```http
GET /api/v1/patrimoines/nearby/?lat=48.8566&lng=2.3522&radius=5&limit=50
```
**Retour optimisé pour la carte**

### 4. **Détails Complets**
```http
GET /api/v1/patrimoines/{id}/full
```
**Toutes les informations pour le popup**

## 🔧 Améliorations API Suggérées

### 1. **Endpoint dédié carte**
```python
# api/views/patrimoine_views.py
class PatrimoineMapView(generics.ListAPIView):
    """Endpoint optimisé pour les cartes Angular"""
    queryset = Patrimoine.objects.all()
    serializer_class = PatrimoineMapSerializer
    
    def get_queryset(self):
        return Patrimoine.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
```

### 2. **Serializer pour carte**
```python
# api/serializers/serializers.py
class PatrimoineMapSerializer(serializers.ModelSerializer):
    """Serializer léger pour les cartes"""
    popup_content = serializers.SerializerMethodField()
    
    class Meta:
        model = Patrimoine
        fields = ['id', 'nom', 'lat', 'lng', 'type', 'ville', 'photo_url', 'popup_content']
    
    def get_popup_content(self, obj):
        return f"<strong>{obj.nom}</strong><br>{obj.ville}<br>{obj.type}"
```

### 3. **CORS Configuration**
```python
# config/settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular dev server
    "http://localhost:3000",  # React dev server
    "https://votre-domaine.com",
]
```

## 📱 Structure Angular Suggérée

### Services API
```typescript
// src/app/services/heritage.service.ts
@Injectable()
export class HeritageService {
  private apiUrl = 'http://localhost:8005/api/v1';
  
  getSitesForMap(): Observable<Site[]> {
    return this.http.get<Site[]>(`${this.apiUrl}/patrimoines/map-data`);
  }
  
  getNearbySites(lat: number, lng: number, radius: number): Observable<Site[]> {
    return this.http.get<Site[]>(`${this.apiUrl}/patrimoines/nearby/`, {
      params: { lat, lng, radius }
    });
  }
}
```

### Composants
```typescript
// src/app/components/map/map.component.ts
@Component({
  selector: 'app-heritage-map',
  template: '<div id="map"></div>'
})
export class MapComponent implements OnInit {
  sites: Site[] = [];
  
  constructor(private heritageService: HeritageService) {}
  
  ngOnInit() {
    this.loadSites();
  }
  
  loadSites() {
    this.heritageService.getSitesForMap().subscribe(sites => {
      this.sites = sites;
      this.initMap();
    });
  }
}
```

## 🚀 Conclusion

**NON, vous n'avez pas besoin de la carte Django !**

Pour Angular :
1. ✅ **API pure** - endpoints REST optimisés
2. ✅ **CORS configuré** - autoriser Angular
3. ✅ **Données légères** - pour les performances
4. ✅ **JWT auth** - pour la sécurité

Angular gérera :
- 🗺️ **Leaflet/Mapbox** dans les composants
- 🔍 **Filtres** dans les formulaires
- 📍 **Géolocalisation** avec le navigateur
- 📱 **Interface responsive**
