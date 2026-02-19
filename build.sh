#!/usr/bin/env bash
echo "🚀 DÉBUT DU DÉPLOIEMENT GEOHERITAGE BACKEND"
echo "📦 Installation des dépendances..."
pip install -r requirements.txt
echo "✅ Dépendances installées"

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input
echo "✅ Fichiers statiques collectés"

echo "🗄️ Migration de la base de données..."
python manage.py migrate
echo "✅ Base de données migrée"

echo "👤 Vérification de l'utilisateur admin..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if User.objects.filter(username='admin').exists():
    admin = User.objects.get(username='admin')
    print(f'✅ Admin trouvé: {admin.username} (is_superuser={admin.is_superuser}, is_staff={admin.is_staff})')
else:
    print('❌ Admin non trouvé')
"

echo "🎯 DÉPLOIEMENT TERMINÉ AVEC SUCCÈS"
echo "🌐 L'application sera disponible sous peu"
