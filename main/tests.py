import pytest
from rest_framework.test import APIClient
from main.models import Don, Contact, Action


@pytest.mark.django_db
class TestDonViewSetSecurity:
    """Vérifie que DonViewSet ne permet que POST (faille corrigée)."""

    def test_get_dons_is_forbidden(self):
        client = APIClient()
        response = client.get('/api/dons/')
        assert response.status_code == 405

    def test_post_don_is_allowed(self):
        client = APIClient()
        response = client.post('/api/dons/', {
            'nom_donateur': 'Test User',
            'email': 'test@example.com',
            'montant': '50.00',
            'anonyme': False,
        })
        assert response.status_code == 201

    def test_delete_don_is_forbidden(self):
        don = Don.objects.create(
            nom_donateur='Test', email='t@t.com', montant=10
        )
        client = APIClient()
        response = client.delete(f'/api/dons/{don.id}/')
        assert response.status_code == 405

    def test_put_don_is_forbidden(self):
        don = Don.objects.create(
            nom_donateur='Test', email='t@t.com', montant=10
        )
        client = APIClient()
        response = client.put(f'/api/dons/{don.id}/', {
            'nom_donateur': 'Hacked', 'montant': 99999
        })
        assert response.status_code == 405


@pytest.mark.django_db
class TestContactViewSetSecurity:
    """Vérifie que ContactViewSet ne permet que POST."""

    def test_get_contacts_is_forbidden(self):
        client = APIClient()
        response = client.get('/api/contacts/')
        assert response.status_code == 405

    def test_post_contact_is_allowed(self):
        client = APIClient()
        response = client.post('/api/contacts/', {
            'nom': 'Test',
            'email': 'test@example.com',
            'sujet': 'Test sujet',
            'message': 'Test message',
        })
        assert response.status_code == 201


@pytest.mark.django_db
class TestPublicReadOnlyEndpoints:
    """Vérifie que les endpoints publics restent accessibles en lecture."""

    def test_actions_list_accessible(self):
        client = APIClient()
        response = client.get('/api/actions/')
        assert response.status_code == 200

    def test_actions_write_forbidden(self):
        client = APIClient()
        response = client.post('/api/actions/', {'titre': 'Fake action'})
        assert response.status_code in (403, 405)