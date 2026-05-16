from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date, time
from customers.models import Customer
from technicians.models import Technician
from timesheets.models import Timesheet
from core.permissions import Roles
from django.urls import reverse 

User = get_user_model()

class CustomerVisibilityTest(TestCase):
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
        
        self.customer_b = Customer.objects.create(
            contact_person='Bob', company_name='Acme', phone='99999999', address='somewhere'
        )
        self.customer_a = Customer.objects.create(
            contact_person='Alice', company_name='EcmA', phone='8888888', address='wheresome'
        )

        self.timesheet_a = Timesheet.objects.create(
            customer=self.customer_a, technician=self.tech_a,
            job_date=date.today(), issue_reported='x', actions_taken='y',
            start_time=time(9, 0), end_time=time(10, 0)
        )
        self.timesheet_b = Timesheet.objects.create(
            customer=self.customer_b, technician=self.tech_b,
            job_date=date.today(), issue_reported='x', actions_taken='y',
            start_time=time(9, 0), end_time=time(10, 0)
        )
        self.timesheet_repeat = Timesheet.objects.create(
            customer=self.customer_b, technician=self.tech_b,
            job_date=date.today(), issue_reported='x', actions_taken='y',
            start_time=time(9, 0), end_time=time(10, 0)
        )

    def test_admin_can_see_all_customers(self):
        visible = Customer.objects.visible_to(self.admin)
        self.assertEqual(visible.count(),2)

    def test_technician_cant_see_customers_not_assigned_to_them(self):
        visible_a = Customer.objects.visible_to(self.tech_user_a)
        visible_b = Customer.objects.visible_to(self.tech_user_b)
        

        self.assertIn(self.customer_a, visible_a)
        self.assertNotIn(self.customer_b, visible_a)
        self.assertIn(self.customer_b, visible_b)
        self.assertNotIn(self.customer_a, visible_b)


    def test_technician_can_only_see_customers_assigned_to_them_in_view(self):
        self.client.login(username='techa' , password='pw')
        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 200)
        customers_in_response=response.context['customers']
        self.assertEqual(customers_in_response.count(),1)
        self.assertIn(self.customer_a,customers_in_response)
        self.assertNotIn(self.customer_b,customers_in_response)

        self.client.login(username='techb' , password='pw')
        response = self.client.get(reverse('customer_list'))

        self.assertEqual(response.status_code, 200)
        customers_in_response=response.context['customers']
        self.assertEqual(customers_in_response.count(),1)
        self.assertIn(self.customer_b,customers_in_response)
        self.assertNotIn(self.customer_a,customers_in_response)
