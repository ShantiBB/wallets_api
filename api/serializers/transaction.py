from django.db import transaction
from rest_framework import serializers

from wallet.models import Wallet
from api.service import update_balance
from api.serializers.validations import (
    valid_transaction_amount,
    valid_transaction_operation_type
)


class TransactionCreateSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)

    class Meta:
        model = Wallet
        fields = ('id', 'operation_type', 'amount', 'balance')
        extra_kwargs = {
            'balance': {'read_only': True},
        }

    def validate_amount(self, value):
        return valid_transaction_amount(self, value)

    @staticmethod
    def validate_operation_type(value):
        return valid_transaction_operation_type(value)

    @transaction.atomic
    def create(self, validated_data):
        wallet = self.context['wallet']
        operation_type = validated_data.get('operation_type')
        amount = validated_data.get('amount')
        new_balance = update_balance(wallet, operation_type, amount)
        validated_data['balance'] = new_balance

        return validated_data
