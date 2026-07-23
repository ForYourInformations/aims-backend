from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'actions',    views.ActionViewSet,       basename='action')
router.register(r'dons',       views.DonViewSet,          basename='don')
router.register(r'contacts',   views.ContactViewSet,      basename='contact')
router.register(r'bureau',     views.MembreBureauViewSet, basename='bureau')
router.register(r'bilans',     views.BilanAnnuelViewSet,  basename='bilan')
router.register(r'actualites', views.ActualiteViewSet,    basename='actualite')
router.register(r'config',     views.ConfigurationViewSet, basename='config')

urlpatterns = [
    path('', include(router.urls)),
    path('home/', views.home_data, name='home-data'),
]

# ── Endpoints générés automatiquement ────────────────────────────────────────
# GET  /api/                    → racine navigable (DRF browser)
# GET  /api/actions/            → liste actions
# GET  /api/actions/{id}/       → détail action
# GET  /api/actions/?categorie= → filtre
# POST /api/dons/               → créer un don
# POST /api/contacts/           → envoyer un message
# GET  /api/bureau/             → membres du bureau
# GET  /api/bilans/             → tous les bilans
# GET  /api/bilans/stats/       → résumé pour accueil
# GET  /api/actualites/         → actualités publiées
# GET  /api/home/               → données complètes accueil
