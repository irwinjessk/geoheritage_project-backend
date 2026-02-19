from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        print("🔧 Démarrage de l'application Account")
        import account.signals
        print("✅ Signals Account chargés")
