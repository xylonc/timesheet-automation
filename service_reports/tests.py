from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date, time
from customers.models import Customer
from technicians.models import Technician
from .models import ServiceReport
from core.permissions import Roles
from django.urls import reverse 

User = get_user_model()

class ServiceReportVisibilityTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username='admin1', password='pw')
        self.admin.groups.add(Group.objects.get(name=Roles.ADMIN))
        
        self.tech_user_a = User.objects.create_user(username='techa', password='pw')
        self.tech_user_a.groups.add(Group.objects.get(name=Roles.TECHNICIAN))
        
        self.tech_user_b = User.objects.create_user(username='techb', password='pw')
        self.tech_user_b.groups.add(Group.objects.get(name=Roles.TECHNICIAN))
        
        self.tech_a = Technician.objects.create(
            user=self.tech_user_a, technician_name='Tech A', tech_phone='11111111'
        )
        self.tech_b = Technician.objects.create(
            user=self.tech_user_b, technician_name='Tech B', tech_phone='22222222'
        )
        
        self.customer = Customer.objects.create(
            contact_person='Bob', company_name='Acme', phone='99999999', address='somewhere'
        )
        self.service_report_a = ServiceReport.objects.create(
            customer=self.customer, technician=self.tech_a,
            job_date=date.today(), issue_reported='x', actions_taken='y',
            start_time=time(9, 0), end_time=time(10, 0)
        )
        self.service_report_b = ServiceReport.objects.create(
            customer=self.customer, technician=self.tech_b,
            job_date=date.today(), issue_reported='x', actions_taken='y',
            start_time=time(9, 0), end_time=time(10, 0)
        )
    
    def test_admin_sees_all_timesheets(self):
        visible = ServiceReport.objects.visible_to(self.admin)
        self.assertEqual(visible.count(), 2)
    
    def test_technician_sees_only_own_timesheets(self):
        visible = ServiceReport.objects.visible_to(self.tech_user_a)
        self.assertEqual(visible.count(), 1)
        self.assertIn(self.service_report_a, visible)
        self.assertNotIn(self.service_report_b, visible)

    def test_superuser_sees_all_timesheets(self):
        superuser = User.objects.create_superuser(username='su', password='pw')
        visible = ServiceReport.objects.visible_to(superuser)
        self.assertEqual(visible.count(), 2)

    def test_technician_see_only_own_timesheet_in_timesheet_list(self):
        self.client.login(username='techa', password='pw')
        response = self.client.get(reverse('service_report_list'))

        self.assertEqual(response.status_code, 200)
        service_reports_in_response = response.context['service_reports']
        self.assertEqual(service_reports_in_response.count(), 1)
        self.assertIn(self.service_report_a, service_reports_in_response)
        self.assertNotIn(self.service_report_b, service_reports_in_response)

