from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from urllib.parse import urlparse, parse_qs
from core.permissions import Roles
from django.contrib.auth.models import Group
from technicians.models import Technician
from unittest.mock import patch

User = get_user_model()

class CreateTechnicianTransactionTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin1', password='pw')
        self.admin.groups.add(Group.objects.get(name=Roles.ADMIN))
        self.client.login(username='admin1', password='pw')
        self.user_count_before = User.objects.count()
        self.tech_count_before = Technician.objects.count()

    def test_invalid_form_no_orphan(self):
        payload = {
            'username': 'newtech',
            'password1': 'somestrongpassword123',
            'password2': 'somestrongpassword123',
            'email': 'newtech@example.com',
            # technician_name omitted on purpose
            'tech_phone': '12345678',
            'is_working': False,
        }
        response = self.client.post(reverse('create_technician'),payload)
        self.assertFalse(User.objects.filter(username='newtech').exists())
        self.assertEqual(Technician.objects.count() ,self.tech_count_before)
        self.assertEqual(response.status_code, 200)

    @patch('technicians.models.Technician.save')
    def test_atomic_rollback_when_technician_save_fails(self, mock_save):
        mock_save.side_effect = Exception("Simulated DB failure")
        
        payload = {
            'username': 'newtech',
            'password1': 'somestrongpassword123',
            'password2': 'somestrongpassword123',
            'email': 'newtech@example.com',
            'technician_name': 'John',
            'tech_phone': '12345678',
            'is_working': False,
        }
        
        with self.assertRaises(Exception):
            self.client.post(reverse('create_technician'), payload)
        
        self.assertFalse(User.objects.filter(username='newtech').exists())
        self.assertEqual(Technician.objects.count(), self.tech_count_before)

