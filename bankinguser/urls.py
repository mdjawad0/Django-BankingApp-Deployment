from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('edit-profile', views.edit_profile, name='edit-profile'),
    path('deactivate', views.deactivate, name='deactivate'),
    path('process-register', views.process_register, name='process-register'),
    path('process-login', views.process_login, name='process-login'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('process-forgot-password', views.process_forgot_password, name='process-forgot-password'),
    path('reset-password', views.reset_password, name='reset-password'),
    path('home', views.home, name='home'),
    path('transaction-requests', views.transaction_requests, name='transaction-requests'),
    path('process-transaction-requests', views.process_transaction_requests, name='process-transaction-requests'),
    path('transaction-history', views.transaction_history, name='transaction-history'),
    path('service-requests', views.service_requests, name='service-requests'),
    path('process-service-requests', views.process_service_requests, name='process-service-requests'),
    path('service-history', views.service_history, name='service-history'),
    path('complaints', views.complaints, name='complaints'),
    path('add-complaint', views.add_complaint, name='add-complaint'),
    path('logout', views.logout, name='logout'),
]