from rest_framework_mongoengine import serializers
from bankingapi.models import CardTransaction

class CardTransactionSerializer(serializers.DocumentSerializer):
    class Meta:
        model = CardTransaction
        fields = ["amount", "transacted_on"]