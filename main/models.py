from django.db import models
from django.utils import timezone


class Action(models.Model):
    CATEGORIE_CHOICES = [
        ('alimentaire', 'Aide alimentaire'),
        ('scolaire', 'Fournitures scolaires'),
        ('medical', 'Aide médicale'),
        ('sensibilisation', 'Sensibilisation'),
        ('fete', 'Fête annuelle'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nb_beneficiaires = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='actions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.titre


class Don(models.Model):
    nom_donateur = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    anonyme = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Don {self.montant}€ — {self.nom_donateur}"


class Contact(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    sujet = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.nom} — {self.sujet}"


class MembreBureau(models.Model):
    ROLE_CHOICES = [
        ('presidente', 'Présidente'),
        ('vice_presidente', 'Vice-Présidente'),
        ('secretaire', 'Secrétaire'),
        ('secretaire_adjoint', 'Secrétaire Adjoint(e)'),
        ('tresoriere', 'Trésorière'),
        ('charges_affaires', "Chargé(e) d'affaires sociales"),
        ('charges_affaires_adj', "Chargé(e) d'affaires sociales adjoint(e)"),
    ]
    nom = models.CharField(max_length=200)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='bureau/', null=True, blank=True)
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} — {self.get_role_display()}"


class BilanAnnuel(models.Model):
    annee = models.IntegerField(unique=True)
    recettes_fete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    recettes_dons = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    depenses_ait = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    depenses_scolaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    solde_banque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    solde_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    nb_enfants_aides = models.IntegerField(default=0)

    class Meta:
        ordering = ['-annee']

    def __str__(self):
        return f"Bilan {self.annee}"

    @property
    def total_recettes(self):
        return float(self.recettes_fete) + float(self.recettes_dons)

    @property
    def total_depenses(self):
        return float(self.depenses_ait) + float(self.depenses_scolaire)

    @property
    def bilan(self):
        return self.total_recettes - self.total_depenses

    @property
    def total_avoirs(self):
        return float(self.solde_banque) + float(self.solde_caisse)


class Actualite(models.Model):
    titre = models.CharField(max_length=300)
    contenu = models.TextField()
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='actualites/', null=True, blank=True)
    publie = models.BooleanField(default=True)
    video_url = models.URLField(
    blank=True, null=True,
    help_text="Collez ici le lien YouTube de la video (exemple: https://www.youtube.com/watch?v=XXXXXXXXX)"
)
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.titre
