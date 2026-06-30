from django.contrib import admin
from .models import Action, Don, Contact, MembreBureau, BilanAnnuel, Actualite

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['titre', 'categorie', 'date', 'montant', 'nb_beneficiaires']
    list_filter = ['categorie']
    search_fields = ['titre']

@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = ['nom_donateur', 'montant', 'date', 'anonyme']
    list_filter = ['anonyme']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'date', 'traite']
    list_editable = ['traite']

@admin.register(MembreBureau)
class MembreBureauAdmin(admin.ModelAdmin):
    list_display = ['nom', 'role', 'ordre']
    list_editable = ['ordre']

@admin.register(BilanAnnuel)
class BilanAnnuelAdmin(admin.ModelAdmin):
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
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date', 'publie', 'a_une_video']
    list_editable = ['publie']
    fieldsets = (
        ('Contenu de l\'actualite', {
            'fields': ('titre', 'date', 'contenu')
        }),
        ('Photo (optionnel)', {
            'fields': ('image',)
        }),
        ('Video YouTube (optionnel)', {
            'fields': ('video_url',),
            'description': 'Filmez avec votre telephone, uploadez la video sur YouTube, '
                            'puis collez le lien ici. Le site affichera la video automatiquement.'
        }),
        ('Publication', {
            'fields': ('publie',),
            'description': 'Cochez cette case quand l\'actualite est prete a etre visible sur le site.'
        }),
    )

    def a_une_video(self, obj):
        return bool(obj.video_url)
    a_une_video.boolean = True
    a_une_video.short_description = 'Video'