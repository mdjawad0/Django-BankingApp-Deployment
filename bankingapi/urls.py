from django.urls import path
from bankingapi.views import (
    BankingAPIView,
)

urlpatterns = [
    path('api', BankingAPIView.as_view()),
]