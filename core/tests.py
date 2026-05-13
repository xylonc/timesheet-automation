from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse 
from urllib.parse import urlparse, parse_qs
from .permissions import Roles
from django.contrib.auth.models import Group

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
    
    def test_authenticated_user_granted_access_protected_view(self):
        """
        Once user is authenticated must not be redirected out
        """
        self.client.login(username='testuser',password='testpass123')

        response = self.client.get(reverse('customer_list'))
        #Catches middelware redirecting an authenticated user
        self.assertNotEqual(response.status_code, 302)

    def test_static_file_request_bypass_middleware(self):
        """
        Static file should be exempted for the styling
        """
        response = self.client.get('/static/css/style.css')

        self.assertNotEqual(response.status_code, 302)

    def test_anonymous_user_can_access_login_page(self):
        """
        Login page must be able accessed by unauthorised users 
        """
        response = self.client.get(reverse('users:login_view'))

        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_anonymous_user_can_access_password_reset(self):
        """
        Login page must be able accessed by unauthorised users 
        """
        response = self.client.get(reverse('users:password_reset'))

        self.assertEqual(response.status_code , 200)
        self.assertTemplateUsed(response, 'users/password_reset.html')


    def test_anonymous_user_redirected_login(self):
        #hit a protected page as unauthenticated user
        response = self.client.get(reverse('customer_list'))

        # Behaviour 1: it's a redirect
        self.assertEqual(response.status_code, 302)
    
        # Behaviour 2: it points to the login page
        parsed = urlparse(response.url)
        self.assertEqual(parsed.path, '/users/login/')
        
        # Behaviour 3: the original destination is preserved
        # Redirected URL contains next param so we must parse the URL
        next_param = parse_qs(parsed.query).get('next', [None])[0]
        self.assertIn('customers', next_param)
    
class RoleRequiredMiddlewareTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='xylonadmin', password='pw12345')
        self.tech = User.objects.create_user(username='xylontech', password='pw12345')
        
        self.admin.groups.add(Group.objects.get(name=Roles.ADMIN))
        self.tech.groups.add(Group.objects.get(name=Roles.TECHNICIAN))

    def test_Admin_access_create_technician(self):
        self.client.login(username="xylonadmin",password="pw12345")

        response = self.client.get(reverse('create_technician'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='technician/create_technician.html')
    
    def test_technician_cannot_access_create_technician(self):
        self.client.login(username='xylontech' , password='pw12345')

        response = self.client.get(reverse('create_technician'))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateNotUsed(response, template_name='technician/create_technician.html')


