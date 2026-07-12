"""
Commande de sauvegarde automatique AIMSEA-DENKO
Usage : python manage.py backup
Planification : cron Render tous les 2 mois
"""
import os
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from io import StringIO


class Command(BaseCommand):
    help = 'Sauvegarde automatique de toutes les données AIMSEA-DENKO'

    def handle(self, *args, **kwargs):
        date     = datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"backup_{date}.json"
        filepath = os.path.join("backups", filename)

        # Créer le dossier backups s'il n'existe pas
        os.makedirs("backups", exist_ok=True)

        # Exporter toutes les données
        self.stdout.write("🔄 Sauvegarde en cours...")
        out = StringIO()
        call_command(
            "dumpdata",
            "--indent", "2",
            "--exclude", "contenttypes",
            "--exclude", "auth.permission",
            "--exclude", "admin.logentry",
            "--exclude", "sessions.session",
            stdout=out,
        )

        # Écrire le fichier
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(out.getvalue())

        size = os.path.getsize(filepath)
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Sauvegarde réussie : {filepath} ({size} octets)"
            )
        )

        # Afficher un résumé
        data = json.loads(out.getvalue())
        models = {}
        for item in data:
            m = item["model"]
            models[m] = models.get(m, 0) + 1

        self.stdout.write("\n📊 Contenu sauvegardé :")
        for model, count in sorted(models.items()):
            self.stdout.write(f"   {model} : {count} enregistrement(s)")