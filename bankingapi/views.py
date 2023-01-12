from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bankingapi.models import *
from django.core.mail import send_mail
from bankingapi.serializers import CardTransactionSerializer

import datetime

class BankingAPIView(APIView):

    # 1. List all Card Transactions
    def get(self, request, *args, **kwargs):
        transactions = CardTransaction.objects
        serializer = CardTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create a Transaction
    """
       {
        "amount": 1000,
        "card": 797787129976,
        "vmonth": 12,
        "vyear": 2025,
        "cvv": 363
       }
    """
    def post(self, request, *args, **kwargs):
        
        amount = int(request.data.get('amount'))
        card_number = int(request.data.get('card'))
        validity_month = int(request.data.get('vmonth'))
        validity_year = int(request.data.get('vyear'))
        cvv = int(request.data.get('cvv'))



        try:
            card = ServiceRequest.objects.get(card_number=card_number, cvv=cvv, status=1)
            
            date_validation = validity_month == card.valid_upto.month and validity_year == card.valid_upto.year
            
            if date_validation == True:

                user = card.requested_by
                account = BankAccount.objects.get(user=user)

                if account.balance > amount:
                    account.balance -= amount
                    account.save()

                    transaction = CardTransaction()
                    transaction.amount = amount
                    transaction.transacted_by = user
                    transaction.account = account
                    transaction.transacted_on = datetime.datetime.now()
                    transaction.save()

                    subject = 'Credit Card Transaction Alert'
                    message = f"Dear {user.name}, \nA Transaction of amount {amount} has been done on your card ending {str(card_number)[-4:]} on {transaction.transacted_on}.\nIf not done by you please contact your bank branch"
                    email_from = 'tuser6794@gmail.com'
                    recipient_list = [user.email, ]
                    send_mail( subject, message, email_from, recipient_list)
                    return Response({'message':'Transaction Successfull'}, status=status.HTTP_201_CREATED)

                else:
                    return Response({'message':'Transaction Failed. Account Balance Low'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'message':'Transaction Failed, Card Details Incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response({'message':'Transaction Failed, Card Details Incorrect'}, status=status.HTTP_400_BAD_REQUEST)
