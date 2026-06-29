from rest_framework import serializers
from .models import Action, Don, Contact, MembreBureau, BilanAnnuel, Actualite


class ActionSerializer(serializers.ModelSerializer):
    categorie_label = serializers.CharField(source='get_categorie_display', read_only=True)

    class Meta:
        model = Action
        fields = [
            'id', 'titre', 'description', 'categorie', 'categorie_label',
            'date', 'montant', 'nb_beneficiaires', 'image', 'created_at',
        ]


class DonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Don
        fields = ['id', 'nom_donateur', 'email', 'montant', 'message', 'date', 'anonyme']
        extra_kwargs = {
            # On ne renvoie jamais l'email au client
            'email': {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.anonyme:
            data['nom_donateur'] = 'Anonyme'
        return data


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'nom', 'email', 'sujet', 'message', 'date']
        read_only_fields = ['date']


class MembreBureauSerializer(serializers.ModelSerializer):
    role_label = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = MembreBureau
        fields = ['id', 'nom', 'role', 'role_label', 'email', 'telephone', 'photo', 'ordre']


class BilanAnnuelSerializer(serializers.ModelSerializer):
    total_recettes = serializers.FloatField(read_only=True)
    total_depenses = serializers.FloatField(read_only=True)
    bilan = serializers.FloatField(read_only=True)
    total_avoirs = serializers.FloatField(read_only=True)

    class Meta:
        model = BilanAnnuel
        fields = [
            'id', 'annee',
            'recettes_fete', 'recettes_dons', 'total_recettes',
            'depenses_ait', 'depenses_scolaire', 'total_depenses',
            'bilan',
            'solde_banque', 'solde_caisse', 'total_avoirs',
            'nb_enfants_aides',
        ]


class ActualiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actualite
        fields = ['id', 'titre', 'contenu', 'date', 'image', 'publie']
