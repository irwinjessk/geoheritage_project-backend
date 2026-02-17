from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Role, UserRole

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
