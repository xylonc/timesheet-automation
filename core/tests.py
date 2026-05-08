from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse 
from urllib.parse import urlparse, parse_qs

User = get_user_model()

class LoginRequiredMiddlewareTest(TestCase):
    """
    Tests for the LoginRequiredMiddleware in core/middleware.py.
    Layer 1 of the auth stack: default-deny authentication.
    """
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_anonymous_user_redirected_login(self):
        #hit a protected page as unauthenticated user
        response = self.client.get('/customers')

        # Behaviour 1: it's a redirect
        self.assertEqual(response.status_code, 302)
    
        # Behaviour 2: it points to the login page
        parsed = urlparse(response.url)
        self.assertEqual(parsed.path, '/users/login/')
        
        # Behaviour 3: the original destination is preserved
        next_param = parse_qs(parsed.query).get('next', [None])[0]
        self.assertIn('customers', next_param)


