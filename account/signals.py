from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError
from .models import Role

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal automatique pour créer le profil utilisateur lors de la création d'un utilisateur.
    """
    if created:
        # Logique à définir lors de la création d'un utilisateur
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal automatique pour sauvegarder le profil utilisateur lors de la sauvegarde d'un utilisateur.
    """
    # Logique à définir lors de la sauvegarde d'un utilisateur
    pass


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """
    Crée un superutilisateur par défaut s'il n'existe pas déjà.
    Se déclenche après chaque migration.
    """
    try:
        if not User.objects.filter(email='admin@gmail.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin'
            )
            print("Superutilisateur par défaut créé avec succès (admin / admin@gmail.com / admin).")
        else:
            print("Le superutilisateur par défaut existe déjà.")
    except OperationalError:
        pass
