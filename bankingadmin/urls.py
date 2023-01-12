from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process-login', views.process_login, name='process-login'),
    path('grant-access', views.grant_access, name='grant-access'),
    path('block-user', views.block_user, name='block-user'),
    path('users', views.users, name='users'),
    path('transactions', views.transactions, name='transactions'),
    path('approve-transaction', views.approve_transaction, name='approve-transaction'),
    path('reject-transaction', views.reject_transaction, name='reject-transaction'),
    path('services', views.services, name='services'),
    path('approve-service', views.approve_service, name='approve-service'),
    path('reject-service', views.reject_service, name='reject-service'),
    path('complaints', views.complaints, name='complaints'),
    path('logout', views.logout, name='logout'),
    path('loan-prediction', views.loan_prediction, name='loan-prediction'),
    path('process-loan-prediction', views.process_loan_prediction, name='process-loan-prediction'), 
]