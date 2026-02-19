from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from account.models import Role


class Command(BaseCommand):
    help = 'Crée un superutilisateur par défaut'

    def handle(self, *args, **options):
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            # Créer le superutilisateur
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin'
            )
            
            # Assigner le rôle admin
            admin_role, created = Role.objects.get_or_create(
                name='admin',
                defaults={
                    'description': 'Administrateur système',
                    'level': 1
                }
            )
            admin_user.roles.add(admin_role)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Superutilisateur admin créé avec rôle admin (level=1)')
            )
        else:
            # Vérifier si l'admin existant a le rôle admin
            admin_user = User.objects.get(username='admin')
            admin_role, _ = Role.objects.get_or_create(
                name='admin',
                defaults={
                    'description': 'Administrateur système',
                    'level': 1
                }
            )
            
            if not admin_user.roles.filter(name='admin').exists():
                admin_user.roles.add(admin_role)
                self.stdout.write(
                    self.style.SUCCESS('✅ Rôle admin assigné à l\'utilisateur admin existant')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('ℹ️ L\'utilisateur admin existe déjà avec le rôle admin')
                )
