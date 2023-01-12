from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from bankingadmin.models import *

class BankingAdminModelTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.get(email='jawad@gmail.com', password='jawad123')
        self.end_user = User.objects.get(email='pjawad786@gmail.com')
        self.transaction = Deposit.objects.get(id='63a071a287b40bc5046180a2')
        self.service = FixedDeposit.objects.get(id='63a40b7fb2be83134331541f')

    def test_admin_login(self):
        self.assertTrue(self.admin_user.name == 'Jawad')

    def test_admin_user_type(self):
        self.assertEquals(self.admin_user.type, 1)

    def test_block_user(self):
        self.end_user.block_user()
        self.assertEquals(self.end_user.status, 0)
        account = BankAccount.objects.get(user=self.end_user)
        self.assertTrue(account.status == 0)

    def test_grant_access_to_user(self):
        message = self.end_user.grant_banking_access()
        self.assertEquals(message, 'Access Granted')

    def test_if_transactions_exists(self):
        transactions = TransactionRequest.objects
        self.assertTrue(len(transactions) > 0)

    def test_deposit_approve(self):
        message = self.transaction.approve()
        self.assertTrue(self.transaction.status == 1)
        self.assertEquals(message, 'Approved')

    def test_deposit_reject(self):
        message = self.transaction.reject()
        self.assertTrue(self.transaction.status == 2)
        self.assertEquals(message, 'Rejected')

    def test_if_services_exists(self):
        services = ServiceRequest.objects
        self.assertTrue(len(services) > 0)

    def test_fixed_deposit_approve(self):
        message = self.service.approve()
        self.assertTrue(self.service.status == 1)
        self.assertEquals(message, 'Approved')

    def test_fixed_deposit_reject(self):
        message = self.service.reject()
        self.assertTrue(self.service.status == 2)
        self.assertEquals(message, 'Rejected')

    def test_if_complaint_exists(self):
        complaints = Complaint.objects
        self.assertTrue(len(complaints) > 0)

class BankingAdminViewTest(TestCase):

    def test_should_show_index_page_if_not_authenticated(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "adminapp/index.html")

    def test_admin_should_login_successfully(self):
        response = self.client.post('/bankingadmin/process-login', {
            'email': 'jawad@gmail.com',
            'password': 'jawad123',
        })

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Admin Login Success", list(map(lambda x: x.message, storage)))

    def test_admin_should_view_all_users(self):
        response = self.client.post('/bankingadmin/process-login', {
            'email': 'jawad@gmail.com',
            'password': 'jawad123',
        })

        response = self.client.get('/bankingadmin/users')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Users Loaded", list(map(lambda x: x.message, storage)))

    def test_admin_should_view_transaction_requests(self):
        response = self.client.post('/bankingadmin/process-login', {
            'email': 'jawad@gmail.com',
            'password': 'jawad123',
        })

        response = self.client.get('/bankingadmin/transactions')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Transactions Loaded", list(map(lambda x: x.message, storage)))

    def test_admin_should_view_service_requests(self):
        response = self.client.post('/bankingadmin/process-login', {
            'email': 'jawad@gmail.com',
            'password': 'jawad123',
        })

        response = self.client.get('/bankingadmin/services')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Services Loaded", list(map(lambda x: x.message, storage)))

    def test_admin_should_view_complaints(self):
        response = self.client.post('/bankingadmin/process-login', {
            'email': 'jawad@gmail.com',
            'password': 'jawad123',
        })

        response = self.client.get('/bankingadmin/complaints')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Complaints Loaded", list(map(lambda x: x.message, storage)))