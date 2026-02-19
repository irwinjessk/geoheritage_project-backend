from django.contrib import admin
from .models import Patrimoine
from django.db.models import Min


@admin.register(Patrimoine)
class PatrimoineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'ville', 'created_by', 'created_at')
    list_filter = ('type', 'ville', 'created_at')
    search_fields = ('nom', 'description', 'ville')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Vérifier les permissions via les rôles
        user_level = request.user.roles.aggregate(min_level=Min('level'))['min_level'] or 999
        
        # Admin (level=1) ou Modérateur (level=2) : voient tout
        if user_level <= 2:
            return qs
        # Contributeur (level=3) : voit seulement ses patrimoines
        elif user_level == 3:
            return qs.filter(created_by=request.user)
        # Utilisateur (level=4+) : ne voit rien
        else:
            return qs.none()
    
    def has_add_permission(self, request):
        user_level = request.user.roles.aggregate(min_level=Min('level'))['min_level'] or 999
        return user_level <= 3  # Contributeur et plus peuvent créer
    
    def has_change_permission(self, request, obj=None):
        user_level = request.user.roles.aggregate(min_level=Min('level'))['min_level'] or 999
        
        # Admin et modo peuvent modifier tout
        if user_level <= 2:
            return True
        # Contributeur peut modifier uniquement ses patrimoines
        elif user_level == 3 and obj and obj.created_by == request.user:
            return True
        return False
    
    def has_delete_permission(self, request, obj=None):
        user_level = request.user.roles.aggregate(min_level=Min('level'))['min_level'] or 999
        
        # Admin et modo peuvent supprimer tout
        if user_level <= 2:
            return True
        # Contributeur peut supprimer uniquement ses patrimoines
        elif user_level == 3 and obj and obj.created_by == request.user:
            return True
        return False
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
