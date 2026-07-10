from django.db import migrations


def update_bilans(apps, schema_editor):
    """
    Mise à jour des bilans selon le tableau corrigé AIMSEA-DENKO (juillet 2026).
    Colonnes : annee, recettes_fete, recettes_dons, depenses_ait, depenses_scolaire, solde_banque
    Source : Tableau_Bilan_Activités_Association_AIMSEA-DENKO.pdf — Marie José Riou
    """
    BilanAnnuel = apps.get_model('main', 'BilanAnnuel')

    bilans_corriges = [
        # annee  fete    dons    ait     scolaire  avoirs
        (2017,   1248,   500,    400,    800,      873.31),
        (2018,   817,    2150,   1090,   600,      1931.09),
        (2019,   0,      2150,   500,    800,      2912.79),
        (2020,   -270,   2450,   1400,   1500,     2394.27),
        (2021,   0,      2400,   450,    1000,     1746.27),
        (2022,   830,    2000,   1000,   1500,     2406.22),
        (2023,   988,    1600,   1000,   1600,     792.19),
        (2024,   1073,   3100,   1150,   2250,     1194.75),
        (2025,   1135,   3600,   1500,   2260,     1079.62),
        (2026,   2040,   0,      0,      0,        0),       # année en cours
    ]

    for annee, rf, rd, da, ds, sb in bilans_corriges:
        BilanAnnuel.objects.update_or_create(
            annee=annee,
            defaults=dict(
                recettes_fete=rf,
                recettes_dons=rd,
                depenses_ait=da,
                depenses_scolaire=ds,
                solde_banque=sb,
            )
        )


def reverse_bilans(apps, schema_editor):
    pass  # pas de rollback automatique


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_seed'),
    ]

    operations = [
        migrations.RunPython(update_bilans, reverse_bilans),
    ]