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
    list_display = ['annee', 'total_recettes', 'total_depenses', 'bilan', 'total_avoirs']

    def total_recettes(self, obj): return f"{obj.total_recettes}€"
    def total_depenses(self, obj): return f"{obj.total_depenses}€"
    def bilan(self, obj): return f"{obj.bilan}€"
    def total_avoirs(self, obj): return f"{obj.total_avoirs}€"

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date', 'publie']
    list_editable = ['publie']

admin.site.site_header = "Administration AIMSEA-DENKO"
admin.site.site_title  = "AIMSEA Admin"
