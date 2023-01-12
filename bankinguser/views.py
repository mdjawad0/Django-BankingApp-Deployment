from django.shortcuts import render
from bankinguser.models import *
from django.core.mail import send_mail
from django.contrib import messages
import hashlib
import datetime
import random

def index(request):
    # return HttpResponse("Welcome to Banking User Application")
    context = {}
    return render(request, 'userapp/index.html', context)

def register(request):
    context = {}
    return render(request, 'userapp/register.html', context)

def profile(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            user = User.objects.get(email=request.session['email'])
            context = {'user':user}
            return render(request, 'userapp/profile.html', context)
    
    context = {}
    return render(request, 'userapp/index.html', context)

def edit_profile(request):
    user = User.objects.get(email=request.session['email'])
    user.name = request.POST['name']
    user.phone = request.POST['phone']
    user.email = request.POST['email']
    old_password = request.POST['password']
    old_password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()

    if user.password == old_password:
        user.password = hashlib.sha256(str(request.POST['newpassword']).encode('utf-8')).hexdigest()
        user.save()
        message = "Profile Successfully Update on {}".format(datetime.datetime.now())
    else:
        message = "Old Password Did Not Match."
    
    context = {'message':message}
    return render(request, 'userapp/message.html', context)

def deactivate(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            user = User.objects.get(email=request.session['email'])
            user.status = 0
            user.save()
            message = "Dear, {}. Your Profile has been deactivated on {}".format(user.name, datetime.datetime.now())
            context = {'message':message}
            return render(request, 'userapp/message.html', context)
    
    context = {}
    return render(request, 'userapp/index.html', context)

def process_register(request):
    if request.method == 'POST':
        user = User()
        user.name = request.POST['name']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.password = hashlib.sha256(str(request.POST['password'])
                        .encode('utf-8')).hexdigest()
        user.type = 2
        user.status = 1
        user.created_on = datetime.datetime.now()
        user.access_status = 0
        user.access_given_on = user.created_on
        user.code = 0
        user.save()
        request.session['email'] = user.email
        context = {'user': user, 'date': datetime.datetime.now().date(), 'time': datetime.datetime.now().time()}
        return render(request, 'userapp/home.html', context)

def process_login(request):
     if request.method == 'POST':
        
        user_email = request.POST['email']
        user_password = hashlib.sha256(str(request.POST['password']).encode('utf-8')).hexdigest()
        
        try:
            user = User.objects.get(email=user_email, password=user_password)
            account = BankAccount.objects.get(user=user)
            request.session['email'] = user.email
            request.session['lastlogin'] = str(datetime.datetime.now())
            messages.add_message(request, messages.SUCCESS, 'User Login Success')
            context = {'user': user, 'account': account, 'date': datetime.datetime.now().date(), 'lastlogin': request.session['lastlogin']}
            return render(request, 'userapp/home.html', context)
       
        except DoesNotExist as error:
            message = "Invalid Login Credentials. Please Try Again"
            messages.add_message(request, messages.ERROR, 'User Login Failed')
            context = {'message': message}
            return render(request, 'userapp/message.html', context)

def home(request):
    if request.session.has_key('email'):
        if len(request.session['email']) > 0:
            user = User.objects.get(email=request.session['email'])
            try:
                account = BankAccount.objects.get(user=user)
                context = {'user':user, 'account':account, 'date': datetime.datetime.now().date(), 'lastlogin': request.session['lastlogin']}
            except DoesNotExist as error:
                context = {'user':user, 'date': datetime.datetime.now().date(), 'lastlogin': request.session['lastlogin']}
            
            return render(request, 'userapp/home.html', context)
    
    context = {}
    return render(request, 'userapp/index.html', context)

def transaction_requests(request):
    user = User.objects.get(email=request.session['email'])
    account = BankAccount.objects.get(user=user)
    context = {'account': account}
    return render(request, 'userapp/transaction_requests.html', context)

def forgot_password(request):
    context = {}
    return render(request, 'userapp/forgot_password.html', context)

def process_forgot_password(request):
    user_email = request.POST['email']
    try:
        user = User.objects.get(email=user_email)
        user.code = random.randint(1111,9999)
        user.save()
        subject = 'Password Reset Email'
        message = f'Hi {user.name}, Your Code to Reset Password is: {user.code}'
        email_from = 'tuser6794@gmail.com'
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list)

        context = {'email': user_email}        
        return render(request, 'userapp/reset_password.html', context)
    except DoesNotExist as error:
        context = {'mesage': 'No Account Exists with Email ID {}'.format(user_email)}
        return render(request, 'userapp/message.html', context)

def reset_password(request):
    code = int(request.POST['code'])
    user_email = request.POST['email']
    password = request.POST['password']

    try:
        user = User.objects.get(email=user_email)
        if user.code == code:
            user.password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            user.save()
            context = {'message': 'Password Successfully Reset For Account with Email ID {}'.format(user_email)}
            return render(request, 'userapp/message.html', context)
        else:
            context = {'message': 'Password Reset Failed. Code Mis Matched, Try Again Later.'}
            return render(request, 'userapp/message.html', context)
    except DoesNotExist as error:
        context = {'message': 'Password Reset Failed. Something Went Wrong. Try Again Later.'}
        return render(request, 'userapp/message.html', context)
      

def process_transaction_requests(request):
    if request.method == 'POST':

        user = User.objects.get(email=request.session['email'])
        account = BankAccount.objects.get(user=user)
        if request.POST['type'] == "1" :
            transaction = Deposit()
            transaction.request_type = 1
            transaction.code = random.randint(1111,9999)
            transaction.request_label = "Deposit"
            transaction.requested_by = user
            transaction.requested_on = datetime.datetime.now()
            transaction.status = 0
            transaction.label = "Pending"
            transaction.amount = int(request.POST['amount'])
            transaction.account_number = account.account_number
            transaction.deposited_on = datetime.datetime.now()
            transaction.save()
            subject = "Transaction Update"
            message = f'Hi {user.name}, Deposit Transaction Initiated for amount {transaction.amount} Your Code For Transaction is: {transaction.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            messages.add_message(request, messages.SUCCESS, 'Deposit Request Raised')
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
        elif request.POST['type'] == "2":
            transaction = Withdraw()
            transaction.request_type = 2
            transaction.code = random.randint(1111,9999)
            transaction.request_label = "Withdraw"
            transaction.requested_by = user
            transaction.requested_on = datetime.datetime.now()
            transaction.status = 0
            transaction.label = "Pending"
            transaction.amount = int(request.POST['amount'])
            transaction.account_number = account.account_number
            transaction.withdrawn_on = datetime.datetime.now()
            transaction.save()
            subject = "Transaction Update"
            message = f'Hi {user.name}, Withdraw Transaction Initiated for amount {transaction.amount} Your Code For Transaction is: {transaction.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
        else:
            transaction = Transfer()
            transaction.request_type = 3
            transaction.code = random.randint(1111,9999)
            transaction.request_label = "Transfer"
            transaction.requested_by = user
            transaction.requested_on = datetime.datetime.now()
            transaction.status = 0
            transaction.label = "Pending"
            transaction.amount = int(request.POST['amount'])
            transaction.from_account_number = account.account_number
            transaction.to_account_number = int(request.POST['toaccount'])
            transaction.transferred_on = datetime.datetime.now()
            transaction.save()
            subject = "Transaction Update"
            message = f'Hi {user.name}, Transaction for Transfer Initiated for amount {transaction.amount} Your Code For Transaction is: {transaction.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            context = {'message': message}
            return render(request, 'userapp/message.html', context)

def transaction_history(request):
    user = User.objects.get(email=request.session['email'])
    transactions = TransactionRequest.objects(requested_by=user)
    messages.add_message(request, messages.SUCCESS, 'Transactions Loaded')
    context = {'transactions': transactions}
    return render(request, 'userapp/transaction_history.html', context)

def service_requests(request):
    user = User.objects.get(email=request.session['email'])
    account = BankAccount.objects.get(user=user)
    context = {'account': account}
    return render(request, 'userapp/service_requests.html', context)

def process_service_requests(request):
    if request.method == 'POST':

        user = User.objects.get(email=request.session['email'])
        account = BankAccount.objects.get(user=user)
        if request.POST['type'] == "1" :
            service = FixedDeposit()
            service.request_type = 1
            service.code = random.randint(1111,9999)
            service.request_label = "FixedDeposit"
            service.requested_by = user
            service.requested_on = datetime.datetime.now()
            service.status = 0
            service.label = "Pending"
            service.amount = request.POST['amount']
            service.start_date = request.POST['start_date']
            service.end_date = request.POST['end_date']
            service.fd_account_number = 1234567890
            service.rate_of_interest = 5.5
            service.save()
            subject = "Service Update"
            message = f'Hi {user.name}, Fixed Deposit Service Request Initiated for amount {service.amount} Your Code For Service is: {service.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
        elif request.POST['type'] == "2":
            service = Card()
            service.request_type = 2
            service.code = random.randint(1111,9999)
            service.request_label = "Card"
            service.requested_by = user
            service.requested_on = datetime.datetime.now()
            service.status = 0
            service.label = "Pending"
            service.type = int(request.POST['type'])
            service.card_number = 123412341234
            service.cvv = 1234
            service.valid_upto = datetime.datetime.now()
            service.save()
            subject = "Service Update"
            message = f'Hi {user.name}, Card Service Request Initiated. Your Code For Service is: {service.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
        elif request.POST['type'] == "3":
            service = ChequeBook()
            service.request_type = 3
            service.code = random.randint(1111,9999)
            service.request_label = "ChequeBook"
            service.requested_by = user
            service.requested_on = datetime.datetime.now()
            service.status = 0
            service.label = "Pending"
            service.from_number = 0
            service.to_number = 0
            service.number_of_pages = int(request.POST['number_of_pages'])
            service.save()
            subject = "Service Update"
            message = f'Hi {user.name}, Cheque Book Service Request Initiated for Pages {service.number_of_pages} Your Code For Service is: {service.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
        else:
            service = Loan()
            service.request_type = 4
            service.code = random.randint(1111,9999)
            service.request_label = "Loan"
            service.requested_by = user
            service.requested_on = datetime.datetime.now()
            service.status = 0
            service.label = "Pending"
            service.loan_account_number = 1234567890
            service.amount = request.POST['amount']
            service.start_date = request.POST['start_date']
            service.end_date = request.POST['end_date']
            service.num_of_installments = request.POST['num_of_installments']
            service.rate_of_interest = 10.7
            service.save()
            subject = "Service Update"
            message = f'Hi {user.name}, Loan Service Request Initiated for amount {service.amount} Your Code For Service is: {service.code}'
            email_from = 'tuser6794@gmail.com'
            recipient_list = [user.email, ]
            send_mail( subject, message, email_from, recipient_list)
            messages.add_message(request, messages.SUCCESS, 'Loan Request Raised')
            context = {'message': message}
            return render(request, 'userapp/message.html', context)
   
def service_history(request):
    user = User.objects.get(email=request.session['email'])
    services = ServiceRequest.objects(requested_by=user)
    messages.add_message(request, messages.SUCCESS, 'Services Loaded')
    context = {'services': services}
    return render(request, 'userapp/service_history.html', context)

def complaints(request):
    context = {}
    return render(request, 'userapp/complaints.html', context)

def add_complaint(request):
    if request.method == 'POST':
        complaint = Complaint()
        user = User.objects.get(email=request.session['email'])
        complaint.raised_by = user
        complaint.user_email = user.email
        complaint.user_phone = user.phone
        complaint.title = request.POST['title']
        complaint.description = request.POST['description']
        complaint.raised_on = datetime.datetime.now()
        complaint.save()
        messages.add_message(request, messages.SUCCESS, 'Complaint Raised')
        context = {'message': "Thank You, {}. Your Complaint has been raised on {}. Our Team shall reach you shortly.".format(user.name, complaint.raised_on)}
        return render(request, 'userapp/message.html', context)


def logout(request):
    request.session['email'] = ""
    context = {}
    return render(request, 'userapp/index.html', context)
