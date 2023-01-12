from django.db import models
from mongoengine import *

# Create your models here.
disconnect()
connect(
    host="mongodb+srv://jawad:jawad123@cluster0.zsnblev.mongodb.net/?retryWrites=true&w=majority",
    db="mydb"
    )

class User(Document):
    name = StringField(required=True)
    phone = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    type = IntField(required=True) # 1 for bank admin user, 2 for end user
    status = IntField(required=True)  # 0 for blocked, 1 for active
    access_status = IntField(required=True)  # 0 for no access, 1 for access given
    access_updated_on = DateTimeField()
    created_on = DateTimeField(required=True)
    code = IntField()

    def deactivate(self):
        self.status = 0
        self.save()
        return "Deactivated"


class BankAccount(Document):
    account_number = IntField(required=True)
    balance = IntField(required=True)
    created_on = DateTimeField(required=True)
    last_updated_on = DateTimeField(required=True)
    status = IntField(required=True) # 0 for blocked, 1 for active
    user = ReferenceField(User)


class TransactionRequest(Document):
    request_type = IntField(required=True)
    request_label = StringField(required=True)
    requested_by = ReferenceField(User)
    code = IntField(required=True)
    requested_on = DateTimeField(required=True)
    status = IntField(required=True)
    label = StringField(required=True)
    meta = {'allow_inheritance': True}


class Deposit(TransactionRequest):
    amount = IntField(required=True)
    account_number = IntField(required=True)
    deposited_on = DateTimeField(required=True)


class Withdraw(TransactionRequest):
    amount = IntField(required=True)
    account_number = IntField(required=True)
    withdrawn_on = DateTimeField(required=True)


class Transfer(TransactionRequest):
    amount = IntField(required=True)
    from_account_number = IntField(required=True)
    to_account_number = IntField(required=True)
    transferred_on = DateTimeField(required=True)


class ServiceRequest(Document):
    request_type = IntField(required=True) # 1 for fixed deposit, 2 for debit/credit card, 3 for cheque book, 4 for loan
    request_label = StringField(required=True)
    requested_by = ReferenceField(User)
    code = IntField(required=True)
    requested_on = DateTimeField(required=True)
    status = IntField(required=True) # 0 for pending, 1 for approved, 2 for rejected
    label = StringField(required=True)
    meta = {'allow_inheritance': True}


class FixedDeposit(ServiceRequest):
    fd_account_number = IntField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    amount = IntField(required=True)
    rate_of_interest = FloatField(required=True)
    status = IntField(required=True) # 1 for active, 2 for finished


class Card(ServiceRequest):
    card_number = IntField(required=True)
    valid_upto = DateTimeField(required=True)
    cvv = IntField(required=True)
    type = IntField(required=True)
    status = IntField(required=True) # 0 for blocked=None, 1 for active


class ChequeBook(ServiceRequest):
    from_number = IntField(required=True)
    to_number = IntField(required=True)
    number_of_pages = IntField(required=True)
    status = IntField(required=True) # 0 for blocked, 1 for active


class Loan(ServiceRequest):
    loan_account_number = IntField(required=True)
    amount = IntField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    num_of_installments = IntField(required=True)
    rate_of_interest = FloatField(required=True)
    status = IntField(required=True) # 1 for active, 2 for finished


class Complaint(Document):
    raised_by = ReferenceField(User)
    user_email = StringField(required=True)
    user_phone = StringField(required=True)
    title = StringField(required=True)
    description = StringField(required=True)
    raised_on = DateTimeField(required=True)