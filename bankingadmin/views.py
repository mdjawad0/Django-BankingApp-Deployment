from django.shortcuts import render
from bankingadmin.models import *
from django.core.mail import send_mail
from django.contrib import messages
import datetime
import boto3
import random
import json

account_counter = 100000
loan_account_counter = 300000
fd_account_counter = 500000


def index(request):
    # return HttpResponse("Welcome to Banking Admin Application")
    context = {}
    return render(request, 'adminapp/index.html', context)

def process_login(request):
     if request.method == 'POST':
        user_email = request.POST['email']
        user_password = request.POST['password']
        try:
            user = User.objects.get(email=user_email, password=user_password)
            users = User.objects
            request.session['email'] = user.email
            context = {'users': users, 'name': user.name, 'email': user.email, 'datetime':datetime.datetime.now()}
            messages.add_message(request, messages.SUCCESS, 'Admin Login Success')
            return render(request, 'adminapp/users.html', context)
        except DoesNotExist as error:
            message = "Invalid Login Credentials. Please Try Again"
            messages.add_message(request, messages.ERROR, 'Admin Login Failed')
            context = {'message': message}
            return render(request, 'adminapp/message.html', context)

def grant_access(request):

     if request.method == 'GET':
        user_email = request.GET['email']
        user = User.objects.get(email=user_email)
        user.access_status = int(request.GET['status'])
        user.access_given_on = datetime.datetime.now()
        user.save()

        try:
            account = BankAccount.objects.get(user=user.id)
            account.status = int(request.GET['status'])
            account.last_updated_on = datetime.datetime.now()
            account.save()
            message = "Dear {}, You have been granted access to bank account # {} again with balance of INR {}".format(user.name, account.account_number, account.balance)
        except:
            account = BankAccount()
            account.account_number = account_counter + len(User.objects)
            account.balance = 10000
            account.created_on = datetime.datetime.now()
            account.last_updated_on = datetime.datetime.now()
            account.status = int(request.GET['status'])
            account.user = user
            account.save()
            message = "Dear {}, You have been granted the access to bank account # {} with a new balance of INR {}".format(user.name, account.account_number, account.balance)

        if account.status == 0:
            message = "Dear {}, Access revoked for bank account # {} with balance of INR {}".format(user.name, account.account_number, account.balance)
        
        subject = 'Account Access Update'
        email_from = 'tuser6794@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list)

        context = {'message': message}
        return render(request, 'adminapp/message.html', context)

def block_user(request):

     if request.method == 'GET':
        user_email = request.GET['email']
        user = User.objects.get(email=user_email)
        user.status = int(request.GET['status'])
        user.save()
        account = BankAccount.objects.get(user=user.id)
        account.status = int(request.GET['status'])
        account.last_updated_on = datetime.datetime.now()
        account.save()
        
        if user.status == 0:        
            message = "{}'s account has been blocked successfully on {}".format(user.name, datetime.datetime.now())
        else:
            message = "{}'s account has been unblocked successfully on {}".format(user.name, datetime.datetime.now())

        subject = 'Account Status Update'
        email_from = 'tuser6794@gmail.com'
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)

        context = {'message': message}
        return render(request, 'adminapp/message.html', context)


def users(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            user = User.objects.get(email=request.session['email'])
            users = User.objects
            context = {'users': users, 'name': user.name, 'email': user.email, 'datetime':datetime.datetime.now()}
            messages.add_message(request, messages.SUCCESS, 'Users Loaded')
            return render(request, 'adminapp/users.html', context)    
    
    context = {}
    return render(request, 'adminapp/index.html', context)
    

def transactions(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            transactions = TransactionRequest.objects
            context = {'transactions': transactions}
            messages.add_message(request, messages.SUCCESS, 'Transactions Loaded')
            return render(request, 'adminapp/transactions.html', context)
    
    context = {}
    return render(request, 'adminapp/index.html', context)


def approve_transaction(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
             if request.method == 'GET':
                if request.GET['type'] == '1':
                    tid = request.GET['tid']
                    transaction = TransactionRequest.objects.get(id=tid)
                    user = transaction.requested_by
                    
                    account = BankAccount.objects.get(user=user)
                    account.balance += transaction.amount
                    account.last_updated_on = datetime.datetime.now()
                    account.save()
                    
                    transaction.label = "Approved"
                    transaction.status = 1
                    transaction.deposited_on = datetime.datetime.now()
                    transaction.save()
                    message = "{}'s account has been credited successfully on {} New Balance is: {}".format(user.name, datetime.datetime.now(), account.balance)
                
                elif request.GET['type'] == '2':
                    tid = request.GET['tid']
                    transaction = TransactionRequest.objects.get(id=tid)
                    user = transaction.requested_by
                    
                    account = BankAccount.objects.get(user=user)
                    account.balance -= transaction.amount
                    account.last_updated_on = datetime.datetime.now()
                    account.save()
                    
                    transaction.label = "Approved"
                    transaction.status = 1
                    transaction.withdrawn_on = datetime.datetime.now()
                    transaction.save()
                   
                    message = "{}'s account has been debited successfully on {} New Balance is: {}".format(user.name, datetime.datetime.now(), account.balance)

                else:
                    tid = request.GET['tid']
                    transaction = TransactionRequest.objects.get(id=tid)
                    user = transaction.requested_by
                    account = BankAccount.objects.get(user=user)
                    account.balance -= transaction.amount
                    account.last_updated_on = datetime.datetime.now()
                    account.save()

                    account = BankAccount.objects.get(account_number=transaction.to_account_number)
                    account.balance += transaction.amount
                    account.last_updated_on = datetime.datetime.now()
                    account.save()

                    transaction.label = "Approved"
                    transaction.status = 1
                    transaction.transferred_on = datetime.datetime.now()
                    transaction.save()
                    message = "{}'s account has been debited successfully for a Transfer on {} New Balance is: {}".format(user.name, datetime.datetime.now(), account.balance)


                subject = 'Transaction Approved'
                email_from = 'tuser6794@gmail.com'
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                context = {'message': message}
                return render(request, 'adminapp/message.html', context)

    context = {}
    return render(request, 'adminapp/index.html', context)

def reject_transaction(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
             
             if request.method == 'GET':
                tid = request.GET['tid']
                transaction = TransactionRequest.objects.get(id=tid)
                user = transaction.requested_by
                    
                transaction.label = "Rejected"
                transaction.status = 2
                transaction.save()
                    
                message = "{} Transaction for {} has been rejected on {}".format(transaction.request_label, user.name, datetime.datetime.now())

                subject = 'Transaction Rejected'
                email_from = 'tuser6794@gmail.com'
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                context = {'message': message}
                return render(request, 'adminapp/message.html', context)
    
    context = {}
    return render(request, 'adminapp/index.html', context)

def services(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            services = ServiceRequest.objects
            context = {'services': services}
            messages.add_message(request, messages.SUCCESS, 'Services Loaded')
            return render(request, 'adminapp/services.html', context)

    context = {}
    return render(request, 'adminapp/index.html', context)


def approve_service(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
             if request.method == 'GET':
                if request.GET['type'] == '1':
                    sid = request.GET['sid']
                    service = ServiceRequest.objects.get(id=sid)
                    user = service.requested_by
                    
                    
                    service.label = "Approved"
                    service.status = 1
                    # Grant FD Number
                    service.fd_account_number = fd_account_counter + len(ServiceRequest.objects(request_type=1, status=1))
                    service.save()
                    message = "{}'s Fixed Deposit Account with Number {} has been approved with Rate of Interest {}".format(user.name, service.fd_account_number, service.rate_of_interest)
                
                elif request.GET['type'] == '2':
                    sid = request.GET['sid']
                    service = ServiceRequest.objects.get(id=sid)
                    user = service.requested_by
                    
                    service.label = "Approved"
                    service.status = 1
                    # Grant Card number Details
                    service.card_number = random.randint(111111111111,999999999999)
                    service.cvv = random.randint(111, 999)
                    service.valid_upto = datetime.datetime.now() + datetime.timedelta(days=3*365)
                    service.save()
                    message = "{}'s Card Book with Number {} has been approved with CVV {}".format(user.name, service.card_number, service.cvv)
                
                elif request.GET['type'] == '3':
                    sid = request.GET['sid']
                    service = ServiceRequest.objects.get(id=sid)
                    user = service.requested_by
                    
                    
                    service.label = "Approved"
                    service.status = 1
                    # Grant cheque Book Number
                    service.from_number = random.randint(1111,9999)
                    service.to_number = service.from_number + service.number_of_pages
                    service.save()
                    message = "{}'s Cheque Book with Pages {} has been approved with Page Number Starting From {}".format(user.name, service.number_of_pages, service.from_number)
                

                else:
                    sid = request.GET['sid']
                    service = ServiceRequest.objects.get(id=sid)
                    user = service.requested_by
                    
                    service.label = "Approved"
                    service.status = 1
                    # Grant Loan Number
                    service.loan_account_number = loan_account_counter + len(ServiceRequest.objects(request_type=4, status=1))
                    service.save()
                    message = "{}'s Loan Account with Number {} has been approved with Rate of Interest {}".format(user.name, service.loan_account_number, service.rate_of_interest)
                

                subject = 'Service Approved'
                email_from = 'tuser6794@gmail.com'
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                context = {'message': message}
                return render(request, 'adminapp/message.html', context)

    context = {}
    return render(request, 'adminapp/index.html', context)

def reject_service(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
             
             if request.method == 'GET':
                sid = request.GET['sid']
                service = ServiceRequest.objects.get(id=sid)
                user = service.requested_by
                    
                service.label = "Rejected"
                service.status = 2
                service.save()
                    
                message = "{} Service for {} has been rejected on {}".format(service.request_label, user.name, datetime.datetime.now())

                subject = 'Service Rejected'
                email_from = 'tuser6794@gmail.com'
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)

                context = {'message': message}
                return render(request, 'adminapp/message.html', context)
    
    context = {}
    return render(request, 'adminapp/index.html', context)


def complaints(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            complaints = Complaint.objects
            context = {'complaints': complaints}
            messages.add_message(request, messages.SUCCESS, 'Complaints Loaded')
            return render(request, 'adminapp/complaints.html', context)

    context = {}
    return render(request, 'adminapp/index.html', context)


def logout(request):
    request.session['email'] = ""
    context = {}
    return render(request, 'adminapp/index.html', context)

def loan_prediction(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            context = {'complaints': complaints}
            return render(request, 'adminapp/loanprediction.html', context)
    
    context = {}
    return render(request, 'adminapp/index.html', context)

def process_loan_prediction(request):

    gender = int(request.POST['gender'])
    married = int(request.POST['married'])
    dependents = int(request.POST['dependents'])
    education = int(request.POST['education'])
    employed = int(request.POST['employed'])
    income = int(request.POST['income'])
    coincome = int(request.POST['coincome'])
    amount = int(request.POST['amount'])
    term = int(request.POST['term'])
    credit = int(request.POST['credit'])
    area = int(request.POST['area'])

    # Specify the EndPoint 
    ENDPOINT_NAME = 'sagemaker-xgboost-2022-12-30-12-09-28-291'

def process_loan_prediction(request):

    gender = int(request.POST['gender'])
    married = int(request.POST['married'])
    dependents = int(request.POST['dependents'])
    education = int(request.POST['education'])
    employed = int(request.POST['employed'])
    income = int(request.POST['income'])
    coincome = int(request.POST['coincome'])
    amount = int(request.POST['amount'])
    term = int(request.POST['term'])
    credit = int(request.POST['credit'])
    area = int(request.POST['area'])

    # Specify the EndPoint 
    ENDPOINT_NAME = 'sagemaker-xgboost-2023-01-09-08-07-05-195'

    # Initialize the Sagemaker Client
    runtime = boto3.client('runtime.sagemaker', 
        region_name='us-east-1',
        aws_access_key_id='ASIA4JKKWWZPRCMQZ4GS',
        aws_secret_access_key='TY8h6F/yQpqZ0gtN1WxXrdYcfhsEyM0Bn4vcPg2w',
        aws_session_token='FwoGZXIvYXdzECkaDLxX3yrgkQ5ao6FaOCK+AezpomLRthSNq/tQixkJYpUCMhY15zPuugKrq+1yXkzNZKKvyVY/MFOn9SMSuo9r/SrH073T+xZVNI1+0VjAj/ghMCZN6272zwRaFrbHLJyP2OhgM9O1Hc83qauixf2pRbPIr6jzYtsDCypthw5zFUlZdZBMPX1muSJZdn3AxWce1Ij6sAx0nQHETmNPWHrrxXNzsXbKSCy7jh5AFPAhmolqwEmfwbrUT2mI5FbQyPrxbLgt5ENifwVlx3pR8aEokYfvnQYyLTE/q4EfP3zdBfbGWYNcTCbrNr+Qds9E3G80TdkzB6h688VgsX8xWm+HAgKuFw=='
    )

    # Create the PayLoad
    # data = {'data': '1, 0, 0.0, 0, 0, 5849, 0.0, 0.0, 360.0, 1.0'}
    
    data = {'data': '{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}'.
    format(gender, married, dependents, education, employed, income, coincome, amount, term, credit, area)}

    payload = data['data']
    print(payload)

    # Invoke the Model EndPoint
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME, 
                                        ContentType='text/csv', 
                                        Body=payload)
                                        
    result = json.loads(response['Body'].read().decode())
    percentage = result * 100
    message = "Loan Prediction Result from AWS Sagemaker Machine Learning Model is: {}%".format(percentage)

    context = {'message': message}
    return render(request, 'adminapp/message.html', context)