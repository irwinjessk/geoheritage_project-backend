from django.contrib import admin
from .models import Patrimoine


@admin.register(Patrimoine)
class PatrimoineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'ville', 'created_by', 'created_at')
    list_filter = ('type', 'ville', 'created_at')
    search_fields = ('nom', 'description', 'ville')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
            print(f"🆕 Création du patrimoine '{obj.nom}' par {request.user.username}")
        else:  # Si c'est une modification
            print(f"✏️ Modification du patrimoine '{obj.nom}' par {request.user.username}")
        super().save_model(request, obj, form, change)
    
    def delete_model(self, request, obj):
        print(f"🗑️ Suppression du patrimoine '{obj.nom}' par {request.user.username}")
        super().delete_model(request, obj)
