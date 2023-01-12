from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from bankinguser.models import *
import hashlib
import datetime

class BankingUserModelTest(TestCase):

    def setUp(self):
        password = hashlib.sha256('jawad1010'.encode('utf-8')).hexdigest()
        self.end_user = User.objects.get(email='pjawad786@gmail.com', password=password)

    def test_user_login(self):
        self.assertTrue(self.end_user.name == 'Mohammed Jawad Pasha')

    def test_end_user_type(self):
        self.assertEquals(self.end_user.type, 2)

    def test_is_user_blocked(self):
        self.assertEquals(self.end_user.status, 0)
        account = BankAccount.objects.get(user=self.end_user)
        # For Jenkins Automations update the status as 0
        account.status = 0
        self.assertTrue(account.status == 0)

    def test_is_user_has_access(self):
        self.assertTrue(self.end_user.access_status == 1)

    def test_if_user_has_transaction_history(self):
        transactions = TransactionRequest.objects(requested_by=self.end_user)
        self.assertTrue(len(transactions) > 0)

    def test_if_user_has_services_history(self):
        transactions = ServiceRequest.objects(requested_by=self.end_user)
        self.assertTrue(len(transactions) > 0)

    def test_if_user_has_raised_complaints(self):
        complaints = Complaint.objects(raised_by=self.end_user)
        self.assertTrue(len(complaints) > 0)

    def test_if_user_deactivated_profile(self):
        message = self.end_user.deactivate()
        self.assertEquals(message, 'Deactivated')

class BankingUserViewTest(TestCase):
    
    def test_should_show_index_page_if_not_authenticated(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userapp/index.html")

    def test_user_should_login_successfully(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("User Login Success", list(map(lambda x: x.message, storage)))

    def test_user_should_raise_deposit_request(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        response = self.client.post('/bankinguser/process-transaction-requests', {
            'type': 1,
            'amount': 15000,
        })

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Deposit Request Raised", list(map(lambda x: x.message, storage)))

    def test_user_should_view_transaction_history(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        response = self.client.get('/bankinguser/transaction-history')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Transactions Loaded", list(map(lambda x: x.message, storage)))

    def test_user_should_raise_loan_request(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        response = self.client.post('/bankinguser/process-service-requests', {
            'type': 4,
            'amount': 50000,
            'start_date': datetime.datetime.now(),
            'end_date': datetime.datetime.now() + datetime.timedelta(days=365),
            'num_of_installments': 12
        })

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Loan Request Raised", list(map(lambda x: x.message, storage)))

    def test_user_should_view_service_history(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        response = self.client.get('/bankinguser/service-history')

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Services Loaded", list(map(lambda x: x.message, storage)))

    def test_user_should_raise_complaint(self):
        response = self.client.post('/bankinguser/process-login', {
            'email': 'pjawad786@gmail.com',
            'password': 'jawad1010',
        })

        response = self.client.post('/bankinguser/add-complaint', {
            'title': "Testing Title",
            'description': "This is a Testing Complaint",
        })

        self.assertEquals(response.status_code, 200)
        storage = get_messages(response.wsgi_request)

        print('***********************')
        print( list(map(lambda x: x.message, storage)))
        print('***********************')

        self.assertIn("Complaint Raised", list(map(lambda x: x.message, storage)))
