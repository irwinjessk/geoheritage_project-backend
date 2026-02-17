# GeoHeritage API

## API REST JWT pour la gestion des patrimoines culturels

### 🎯 Objectifs

- **Authentification JWT** : Sécurité stateless avec tokens
- **Permissions granulaires** : Basées sur les rôles et niveaux
- **CRUD complet** : Création, lecture, mise à jour, suppression
- **Recherche avancée** : Par proximité GPS et filtres multiples

### 🔐 Architecture

```
┌─────────────────┐
│   Frontend    │
├─────────────────┤
│   API JWT     │
├─────────────────┤
│   Django Core   │
└─────────────────┘
```

### 📋 Endpoints

#### Authentification
- `POST /api/auth/login/` - Login avec tokens JWT
- `POST /api/auth/refresh/` - Rafraîchissement du token
- `POST /api/auth/logout/` - Déconnexion (blacklist)
- `GET /api/auth/profile/` - Profil utilisateur avec permissions

#### Patrimoines
- `GET /api/patrimoines/` - Liste paginée avec filtres
- `POST /api/patrimoines/` - Création (contributeur+)
- `GET /api/patrimoines/{id}/` - Détail d'un patrimoine
- `PUT/PATCH /api/patrimoines/{id}/` - Mise à jour (permissions)
- `DELETE /api/patrimoines/{id}/` - Suppression (permissions)
- `GET /api/patrimoines/nearby/` - Recherche par proximité GPS

### 🔐 Sécurité

#### Permissions par niveau
- **Admin (level=1)** : Accès complet à toutes les opérations
- **Modérateur (level=2)** : Modification/suppression de tous les patrimoines
- **Contributeur (level=3)** : Création + modification/suppression de ses patrimoines
- **Utilisateur (level=4)** : Lecture seule

#### Tokens JWT
- **Access Token** : 1 heure de validité
- **Refresh Token** : 24 heures de validité
- **Blacklist** : Tokens invalidés immédiatement

### 🚀 Utilisation

#### Installation
```bash
pip install djangorestframework-simplejwt
```

#### Configuration
```python
# settings.py
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
]

JWT_AUTH = {
    'ACCESS_TOKEN_LIFETIME': 60,
    'REFRESH_TOKEN_LIFETIME': 1440,
    'ROTATE_REFRESH_TOKENS': True,
}
```

#### Exemple d'utilisation
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Créer un patrimoine
curl -X POST http://localhost:8000/api/patrimoines/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"nom": "Notre-Dame", "type": "monument"}'
```

### 📚 Documentation

- **Swagger UI** : `http://localhost:8000/api/docs/`
- **OpenAPI 3.0** : Spécification complète
- **Postman Collection** : Import automatique

### 🧪 Tests

```bash
python manage.py test api.tests.test_jwt_auth
```

### 🔒 Production

- **HTTPS obligatoire** en production
- **Variables environnement** : `SECRET_KEY` et `DJANGO_SETTINGS_MODULE`
- **CORS** : Configuration des domaines autorisés
- **Rate limiting** : Protection contre les abus

---

**API GeoHeritage : Sécurité, performance et évolutivité !** 🏆
