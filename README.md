# AIMSEA-DENKO — Backend Django REST

API REST pour le site web de l'association AIMSEA-DENKO.

## Stack technique

- Django 5.2 + Django REST Framework
- PostgreSQL en production (Railway), SQLite en local
- Gunicorn + WhiteNoise pour la production
- Tests : pytest + pytest-django

## Configuration locale

Copiez le fichier d'exemple et remplissez vos propres valeurs :

```bash
cp .env.example .env
```

Variables requises dans `.env` :

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Cle secrete Django, generer avec `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `True` en local, jamais en production |

Le fichier `.env` ne doit jamais etre commite sur Git — il est deja dans `.gitignore`.

## Installation

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Tests

```bash
pytest
```

## Endpoints API

| Methode | URL | Description |
|---------|-----|-------------|
| GET | `/api/home/` | Donnees page d'accueil |
| GET | `/api/actions/` | Liste des actions |
| GET | `/api/bilans/` | Bilans annuels |
| GET | `/api/bureau/` | Membres du bureau |
| GET | `/api/actualites/` | Actualites publiees |
| POST | `/api/dons/` | Creer un don |
| POST | `/api/contacts/` | Envoyer un message |
| GET | `/admin/` | Interface admin Django |