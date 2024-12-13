from rest_framework import serializers

from wallet.models import Wallet
from services.tasks import wallet_transaction
from api.serializers.validations import (
    valid_transaction_amount,
    valid_transaction_operation_type
)


class TransactionCreateSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(required=True)
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )

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

    def create(self, validated_data):
        wallet = self.context.get('wallet')
        operation_type = validated_data.get('operation_type')
        amount = validated_data.get('amount')
        balance = wallet.balance

        wallet_transaction.delay(
            wallet.id,
            wallet.owner.id,
            balance,
            operation_type,
            amount
        )

        validated_data['id'] = wallet.id
        return validated_data
