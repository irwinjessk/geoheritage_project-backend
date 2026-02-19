from django.core.management.base import BaseCommand
from heritage.models import Patrimoine
from django.test import Client
from django.urls import reverse
import json


class Command(BaseCommand):
    help = 'Diagnostiquer les problèmes de production'

    def handle(self, *args, **options):
        self.stdout.write("🔍 DIAGNOSTIC DE PRODUCTION GEOHERITAGE")
        self.stdout.write("=" * 50)
        
        # 1. Vérifier les données en BDD
        self.stdout.write("\n📊 1. VÉRIFICATION DES DONNÉES")
        total_sites = Patrimoine.objects.count()
        self.stdout.write(f"   • Sites en BDD: {total_sites}")
        
        if total_sites > 0:
            sites = Patrimoine.objects.all()[:5]  # 5 premiers sites
            for i, site in enumerate(sites, 1):
                self.stdout.write(f"   {i}. {site.nom} - {site.ville}")
                self.stdout.write(f"      Photo URL: {site.photo_url}")
                self.stdout.write(f"      Type: {site.type}")
        else:
            self.stdout.write("   ❌ AUCUN SITE TROUVÉ EN BDD")
        
        # 2. Tester les URLs
        self.stdout.write("\n🔗 2. VÉRIFICATION DES URLs")
        try:
            list_url = reverse('heritage:list')
            self.stdout.write(f"   • URL liste: {list_url}")
            
            create_url = reverse('heritage:create')
            self.stdout.write(f"   • URL création: {create_url}")
            
            map_url = reverse('heritage:map')
            self.stdout.write(f"   • URL carte: {map_url}")
        except Exception as e:
            self.stdout.write(f"   ❌ Erreur URLs: {e}")
        
        # 3. Tester les templates
        self.stdout.write("\n📄 3. VÉRIFICATION DES TEMPLATES")
        client = Client()
        
        try:
            response = client.get(reverse('heritage:list'))
            self.stdout.write(f"   • Status liste: {response.status_code}")
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                if 'card-img-top' in content:
                    self.stdout.write("   ✅ Template liste OK")
                else:
                    self.stdout.write("   ⚠️ Template liste modifié")
            else:
                self.stdout.write(f"   ❌ Erreur template: {response.status_code}")
        except Exception as e:
            self.stdout.write(f"   ❌ Erreur template: {e}")
        
        # 4. Vérifier les images
        self.stdout.write("\n🖼️ 4. VÉRIFICATION DES IMAGES")
        if total_sites > 0:
            sites_with_photos = Patrimoine.objects.exclude(photo_url__isnull=True).exclude(photo_url='')
            self.stdout.write(f"   • Sites avec photos: {sites_with_photos.count()}")
            
            for site in sites_with_photos[:3]:  # 3 premiers sites avec photos
                self.stdout.write(f"   • Test image: {site.photo_url}")
                # Note: On ne peut pas tester les URLs externes ici
        
        # 5. Configuration statique
        self.stdout.write("\n⚙️ 5. CONFIGURATION STATIQUE")
        from django.conf import settings
        self.stdout.write(f"   • DEBUG: {settings.DEBUG}")
        self.stdout.write(f"   • STATIC_URL: {settings.STATIC_URL}")
        self.stdout.write(f"   • STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"   • ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        
        # 6. Recommandations
        self.stdout.write("\n💡 6. RECOMMANDATIONS")
        if total_sites == 0:
            self.stdout.write("   ⚠️ Ajoutez des sites via l'admin:")
            self.stdout.write("      1. /admin/")
            self.stdout.write("      2. Connectez-vous avec admin/admin")
            self.stdout.write("      3. Allez dans Patrimoines > Ajouter")
        else:
            self.stdout.write("   ✅ Les données semblent présentes")
            self.stdout.write("   🔍 Vérifiez les logs pour les erreurs d'images")
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("🎯 DIAGNOSTIC TERMINÉ")
