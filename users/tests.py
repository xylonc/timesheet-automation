from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlparse, parse_qs

User = get_user_model()
class CreateAdminSecurityTest(TestCase):
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