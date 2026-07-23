from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Action, Don, Contact, MembreBureau, BilanAnnuel, Actualite, Configuration
from .serializers import ActionSerializer, DonSerializer, ContactSerializer, MembreBureauSerializer, BilanAnnuelSerializer, ActualiteSerializer, ConfigurationSerializer

class ConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
    lookup_field = 'cle'


# ── Actions ───────────────────────────────────────────────────────────────────
class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/actions/           → liste toutes les actions
    GET /api/actions/{id}/      → détail d'une action
    GET /api/actions/?categorie=scolaire → filtre par catégorie
    """
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie']
    search_fields = ['titre', 'description']
    ordering_fields = ['date', 'montant']


# ── Dons ──────────────────────────────────────────────────────────────────────
class DonViewSet(viewsets.ModelViewSet):
    """
    POST /api/dons/     → créer un don (formulaire frontend)
    Lecture, modification et suppression interdites côté public.
    """
    queryset = Don.objects.all()
    serializer_class = DonSerializer
    http_method_names = ['post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        don = serializer.save()
        return Response(
            {
                'message': f'Merci pour votre don de {don.montant}€ ! '
                           f'Votre générosité aide les enfants albinos de Conakry.',
                'don': DonSerializer(don).data,
            },
            status=status.HTTP_201_CREATED,
        )


# ── Contact ───────────────────────────────────────────────────────────────────
class ContactViewSet(viewsets.ModelViewSet):
    """
    POST /api/contacts/  → envoyer un message de contact
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    http_method_names = ['post', 'head', 'options']   # lecture interdite côté public

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Votre message a bien été envoyé. Nous vous répondrons rapidement.'},
            status=status.HTTP_201_CREATED,
        )


# ── Bureau ────────────────────────────────────────────────────────────────────
class MembreBureauViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/bureau/     → liste des membres du bureau
    """
    queryset = MembreBureau.objects.all()
    serializer_class = MembreBureauSerializer


# ── Bilans ────────────────────────────────────────────────────────────────────
class BilanAnnuelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/bilans/     → tous les bilans
    GET /api/bilans/stats/ → résumé global (action personnalisée)
    """
    queryset = BilanAnnuel.objects.all()
    serializer_class = BilanAnnuelSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Résumé rapide pour la page d'accueil"""
        bilans = BilanAnnuel.objects.all()
        dernier = bilans.first()
        return Response({
            'nb_annees': bilans.count(),
            'dernier_bilan': BilanAnnuelSerializer(dernier).data if dernier else None,
            'total_dons_guinee_2025': 3760,
            'nb_enfants_2025': 175,
            'nb_fetes': 7,
        })


# ── Actualités ────────────────────────────────────────────────────────────────
class ActualiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/actualites/  → actualités publiées
    """
    queryset = Actualite.objects.filter(publie=True)
    serializer_class = ActualiteSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['date']


# ── Endpoint global accueil ───────────────────────────────────────────────────
@api_view(['GET'])
def home_data(request):
    """
    GET /api/home/
    Renvoie en une seule requête toutes les données de la page d'accueil
    """
    actions_recentes = Action.objects.all()[:3]
    actualites_recentes = Actualite.objects.filter(publie=True)[:3]
    bilans = BilanAnnuel.objects.all()[:5]
    membres = MembreBureau.objects.all()

    return Response({
        'stats': {
            'annees': 10,
            'enfants_2025': 175,
            'dons_guinee_2025': 3760,
            'fetes': 7,
        },
        'actions_recentes': ActionSerializer(actions_recentes, many=True, context={'request': request}).data,
        'actualites_recentes': ActualiteSerializer(actualites_recentes, many=True, context={'request': request}).data,
        'bilans': BilanAnnuelSerializer(bilans, many=True).data,
        'membres': MembreBureauSerializer(membres, many=True, context={'request': request}).data,
    })
