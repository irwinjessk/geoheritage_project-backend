"""
Tests JWT pour GeoHeritage API
Validation de l'authentification et des permissions
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User, Role
from heritage.models import Patrimoine


User = get_user_model()


class JWTAuthenticationTestCase(APITestCase):
    """
    Tests pour l'authentification JWT
    """
    
    def setUp(self):
        """Configuration des tests"""
        # Créer les rôles de test
        self.admin_role = Role.objects.create(
            name='Administrateur',
            description='Administrateur système',
            level=1
        )
        self.moderator_role = Role.objects.create(
            name='Modérateur',
            description='Modérateur de contenu',
            level=2
        )
        self.contributor_role = Role.objects.create(
            name='Contributeur',
            description='Contributeur de patrimoines',
            level=3
        )
        self.user_role = Role.objects.create(
            name='Utilisateur',
            description='Utilisateur standard',
            level=4
        )
        
        # Créer les utilisateurs de test
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            first_name='Admin',
            last_name='Test',
            password='admin123'
        )
        self.admin_user.roles.add(self.admin_role)
        
        self.moderator_user = User.objects.create_user(
            username='moderator_test',
            email='moderator@test.com',
            first_name='Moderator',
            last_name='Test',
            password='moderator123'
        )
        self.moderator_user.roles.add(self.moderator_role)
        
        self.contributor_user = User.objects.create_user(
            username='contributor_test',
            email='contributor@test.com',
            first_name='Contributor',
            last_name='Test',
            password='contributor123'
        )
        self.contributor_user.roles.add(self.contributor_role)
        
        self.regular_user = User.objects.create_user(
            username='user_test',
            email='user@test.com',
            first_name='User',
            last_name='Test',
            password='user123'
        )
        self.regular_user.roles.add(self.user_role)
    
    def test_admin_can_access_all(self):
        """Test: Admin peut tout faire"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/patrimoines/')
        self.assertEqual(response.status_code, 200)
    
    def test_moderator_can_edit_all(self):
        """Test: Modérateur peut modifier tout"""
        self.client.force_authenticate(user=self.moderator_user)
        response = self.client.get('/api/patrimoines/1/')
        self.assertEqual(response.status_code, 200)
    
    def test_contributor_can_create_and_edit_own(self):
        """Test: Contributeur peut créer et modifier ses patrimoines"""
        self.client.force_authenticate(user=self.contributor_user)
        
        # Test création
        response = self.client.post('/api/patrimoines/', {
            'nom': 'Test Patrimoine',
            'description': 'Test description',
            'type': 'monument',
            'latitude': '48.8566',
            'longitude': '2.3522',
            'ville': 'Paris'
        })
        self.assertEqual(response.status_code, 201)
        
        # Test modification de son patrimoine
        response = self.client.get('/api/patrimoines/1/')
        self.assertEqual(response.status_code, 200)
        
        # Test modification du patrimoine d'un autre
        other_patrimoine = Patrimoine.objects.create(
            nom='Other Patrimoine',
            description='Other description',
            type='monument',
            latitude='48.8566',
            longitude='2.3522',
            ville='Paris',
            created_by=self.admin_user
        )
        response = self.client.patch(f'/api/patrimoines/{other_patrimoine.id}/', {
            'nom': 'Modified by Contributor'
        })
        self.assertEqual(response.status_code, 403)
    
    def test_regular_user_read_only(self):
        """Test: Utilisateur standard peut seulement lire"""
        self.client.force_authenticate(user=self.regular_user)
        
        # Test lecture
        response = self.client.get('/api/patrimoines/')
        self.assertEqual(response.status_code, 200)
        
        # Test création (interdit)
        response = self.client.post('/api/patrimoines/', {
            'nom': 'Test Patrimoine',
            'description': 'Test description',
        })
        self.assertEqual(response.status_code, 403)
    
    def test_unauthenticated_access_denied(self):
        """Test: Accès refusé sans authentification"""
        response = self.client.get('/api/patrimoines/')
        self.assertEqual(response.status_code, 401)
