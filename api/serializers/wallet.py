from django.db import transaction
from rest_framework import serializers

from wallet.models import Wallet
from core.constants import FORMAT
from api.serializers.validations import (
    valid_update_wallet_title_and_description
)

class WalletSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format=FORMAT, read_only=True)
    updated_at = serializers.DateTimeField(format=FORMAT, read_only=True)

    class Meta:
        model = Wallet
        fields = (
            'id',
            'title',
            'description',
            'balance',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'balance': {'read_only': True},
        }


class WalletCreateSerializer(WalletSerializer):

    class Meta(WalletSerializer.Meta):
        fields = ('title', 'description')


class WalletUpdateSerializer(WalletSerializer):
    description = serializers.CharField(required=True)

    def validate(self, attrs):
        valid_update_wallet_title_and_description(self.instance, attrs)
        return attrs

    class Meta(WalletSerializer.Meta):
        fields = ('id', 'title', 'description')

    @transaction.atomic
    def update(self, instance, validated_data):
        wallet_id = instance.get('id')
        title = validated_data.get('title')
        description = validated_data.get('description')

        wallet = Wallet.objects.filter(id=wallet_id).update(
            title=title,
            description=description
        )
        return validated_data
