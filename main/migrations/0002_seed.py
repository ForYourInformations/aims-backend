from django.db import migrations
from datetime import date


def seed(apps, schema_editor):
    BilanAnnuel = apps.get_model('main', 'BilanAnnuel')
    MembreBureau = apps.get_model('main', 'MembreBureau')
    Action = apps.get_model('main', 'Action')
    Actualite = apps.get_model('main', 'Actualite')

    bilans = [
        (2017,1248,0,400,800,1560.31,0,15),
        (2018,817,2150,1000,1500,1886.09,45,0),
        (2019,0,2150,500,800,667.79,2245,0),
        (2020,0,2550,500,1500,1679.27,675,0),
        (2021,0,2400,450,450,1679.27,67,0),
        (2022,830,3210,1000,2500,1901.22,505,0),
        (2023,988,2878,1000,1600,429.19,363,0),
        (2024,1075,4300,1150,2250,1100.75,94,150),
        (2025,1135,5210,1500,2260,935.62,144,175),
    ]
    for a,rf,rd,da,ds,sb,sc,ne in bilans:
        BilanAnnuel.objects.get_or_create(annee=a, defaults=dict(
            recettes_fete=rf, recettes_dons=rd,
            depenses_ait=da, depenses_scolaire=ds,
            solde_banque=sb, solde_caisse=sc,
            nb_enfants_aides=ne,
        ))

    membres = [
        (1,'Mme SIMANKA Nansira','presidente','simanka.nasira@yahoo.fr','06 24 82 08 38'),
        (2,'Mme SYLLA Aicha','vice_presidente','aichasyllakoundia@gmail.com',''),
        (3,'Mme RIOU Marie Jose','secretaire','mjriou@hotmail.fr','06 66 94 96 15'),
        (4,'M. BERETE Sory','secretaire_adjoint','brtsory@gmail.com',''),
        (5,'Mme DIALLO WELLE Mariam','tresoriere','mariamdiallo10s@yahoo.fr',''),
        (6,'M. BERETE Mohamed','charges_affaires','mohamedbeeteer7@gmail.com',''),
        (7,'Mme DIABY Fatoumata','charges_affaires_adj','Fatoumatadiabygp@gmail.com',''),
    ]
    for ordre,nom,role,email,tel in membres:
        MembreBureau.objects.get_or_create(nom=nom, defaults=dict(
            role=role, email=email, telephone=tel, ordre=ordre,
        ))

    actions = [
        ('7eme Fete Annuelle AIMSEA 2025',
         'Fete annuelle pro-fonds. Benefice : 1135 EUR.',
         'fete', date(2025,2,19), 1135.25, 50),
        ('Distribution AIT 2025',
         'Distribution alimentaire a 150 enfants albinos a Conakry.',
         'alimentaire', date(2025,3,27), 1500, 150),
        ('Rentree Scolaire 2025-2026',
         'Fournitures scolaires pour 175 enfants albinos a Conakry.',
         'scolaire', date(2025,10,1), 2260, 175),
        ('Sensibilisation TV en Guinee',
         'Participation a 3 emissions televisees sur la Television Guineenne.',
         'sensibilisation', date(2025,2,19), None, None),
    ]
    for titre,desc,cat,d,montant,ben in actions:
        Action.objects.get_or_create(titre=titre, defaults=dict(
            description=desc, categorie=cat, date=d,
            montant=montant, nb_beneficiaires=ben,
        ))

    actualites = [
        ('AGO du 18 avril 2026',
         'Bilan 2025 approuve a l unanimite. Bureau reconduit pour 2026.',
         date(2026,4,18)),
        ('175 enfants aides en 2025',
         '175 enfants albinos ont recu des fournitures scolaires pour la rentree 2025-2026.',
         date(2025,10,15)),
        ('7eme fete : succes !',
         'La fete du 19 fevrier 2025 a reuni 50 personnes et collecte 3700 EUR de dons.',
         date(2025,2,20)),
    ]
    for titre,contenu,d in actualites:
        Actualite.objects.get_or_create(titre=titre, defaults=dict(
            contenu=contenu, date=d, publie=True,
        ))


class Migration(migrations.Migration):
    dependencies = [('main', '0001_initial')]
    operations = [migrations.RunPython(seed, migrations.RunPython.noop)]