from django.contrib import admin
from django.conf import settings
from django.core.exceptions import PermissionDenied
from .models import Action, Don, Contact, MembreBureau, BilanAnnuel, Actualite, Configuration
from django.contrib.admin.models import LogEntry


class HideHistoryMixin:
    """Cache le bouton Historique aux non-superadmins et masque les actions de lakhdars"""
    def history_view(self, request, object_id, extra_context=None):
        if not request.user.is_superuser:
            raise PermissionDenied
        return super().history_view(request, object_id, extra_context)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message']
    list_filter = ['action_time', 'user', 'action_flag']
    search_fields = ['user__username', 'object_repr']
    readonly_fields = ['action_time', 'user', 'content_type', 'object_id', 'object_repr', 'action_flag', 'change_message']

    def has_module_perms(self, request):
        return request.user.is_superuser

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(user__username='lakhdars')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ['cle', 'valeur', 'description']

    def has_module_perms(self, request):
        return request.user.is_superuser


admin.site.site_header = "Administration AIMSEA-DENKO"
admin.site.site_title  = "AIMSEA Admin"
admin.site.site_url    = settings.SITE_URL


@admin.register(Action)
class ActionAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date', 'montant', 'nb_beneficiaires', 'a_une_video']
    list_filter = ['categorie']
    search_fields = ['titre']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informations principales', {
                'fields': ('titre', 'categorie', 'date', 'description')
            }),
            ('Details', {
                'fields': ('montant', 'nb_beneficiaires', 'image')
            }),
        ]
        if request.user.is_superuser:
            fieldsets.append((
                'Video (optionnel)', {
                    'fields': ('video_url', 'video_file'),
                    'description': 'Deux options : collez un lien YouTube, OU envoyez directement le fichier video '
                                   '(le fichier envoye est prioritaire si les deux sont remplis).'
                }
            ))
        return fieldsets

    def a_une_video(self, obj):
        return bool(obj.video_url or obj.video_file)
    a_une_video.boolean = True
    a_une_video.short_description = 'Video'


@admin.register(Don)
class DonAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['nom_donateur', 'montant', 'date', 'anonyme']
    list_filter = ['anonyme']


@admin.register(Contact)
class ContactAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'date', 'traite']
    list_editable = ['traite']


@admin.register(MembreBureau)
class MembreBureauAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['nom', 'role', 'ordre']
    list_editable = ['ordre']


@admin.register(BilanAnnuel)
class BilanAnnuelAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['annee', 'get_recettes', 'get_depenses', 'get_bilan', 'get_avoirs']

    def get_recettes(self, obj): return f"{obj.total_recettes}€"
    get_recettes.short_description = "Recettes"

    def get_depenses(self, obj): return f"{obj.total_depenses}€"
    get_depenses.short_description = "Dépenses"

    def get_bilan(self, obj): return f"{obj.bilan}€"
    get_bilan.short_description = "Bilan"

    def get_avoirs(self, obj): return f"{obj.total_avoirs}€"
    get_avoirs.short_description = "Avoirs"


@admin.register(Actualite)
class ActualiteAdmin(HideHistoryMixin, admin.ModelAdmin):
    list_display = ['titre', 'date', 'publie', 'a_une_video']
    list_editable = ['publie']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Contenu de l\'actualite', {
                'fields': ('titre', 'date', 'contenu')
            }),
            ('Photo (optionnel)', {
                'fields': ('image',)
            }),
            ('Publication', {
                'fields': ('publie',),
                'description': 'Cochez cette case quand l\'actualite est prete a etre visible sur le site.'
            }),
        ]
        if request.user.is_superuser:
            fieldsets.append((
                'Video (optionnel)', {
                    'fields': ('video_url', 'video_file'),
                    'description': 'Deux options : collez un lien YouTube, OU envoyez directement le fichier video '
                                   '(le fichier envoye est prioritaire si les deux sont remplis). '
                                   'Le site affichera la video automatiquement.'
                }
            ))
        return fieldsets

    def a_une_video(self, obj):
        return bool(obj.video_url or obj.video_file)
    a_une_video.boolean = True
    a_une_video.short_description = 'Video'