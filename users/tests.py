from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlparse, parse_qs
from django.contrib.auth.models import Group
from core.permissions import Roles

User = get_user_model()
class CreateAdminSecurityTest(TestCase):
    def setUp(self):
        self.Admin = User.objects.create_user(username='admin', password='pw')
        self.Admin.groups.add(Group.objects.get(name=Roles.ADMIN))

        self.tech_user = User.objects.create_user(username='techa', password='pw')
        self.tech_user.groups.add(Group.objects.get(name=Roles.TECHNICIAN))

    def test_anonymous_post_to_create_admin_does_not_create_user(self):
        payload = {
            'username': 'attacker',
            'password1': 'somestrongpassword123',
            'password2': 'somestrongpassword123',
            'email': 'attacker@example.com',
        }
        response = self.client.post(reverse('users:create_admin'), payload)
        
        self.assertFalse(User.objects.filter(username='attacker').exists())
        self.assertEqual(response.status_code, 302)
        #Redirect URL has the next param so we must parse the input 
        parsed = urlparse(response.url)
        self.assertEqual(parsed.path, '/users/login/')
        next_param = parse_qs(parsed.query).get('next', [None])[0]
        self.assertIn('create_admin', next_param)

    def test_user_logouts_using_get_will_405(self):
        self.client.login(username='admin',password='pw')
        response = self.client.get(reverse('users:logout_view'))

        self.assertEqual(response.status_code , 405)

