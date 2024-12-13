from django.db import transaction
from rest_framework import serializers
from djoser.serializers import UserSerializer

from wallet.models import Wallet
from core.constants import FORMAT
from api.serializers.validations import (
    valid_update_wallet_title_and_description
)


class WalletListSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Wallet
        fields = (
            'id',
            'title',
            'balance',
            'owner',
        )
        extra_kwargs = {
            'balance': {'read_only': True},
        }


class WalletDetailSerializer(WalletListSerializer):
    created_at = serializers.DateTimeField(format=FORMAT, read_only=True)
    updated_at = serializers.DateTimeField(format=FORMAT, read_only=True)

    class Meta(WalletListSerializer.Meta):
        fields = (
            'id',
            'title',
            'description',
            'balance',
            'owner',
            'created_at',
            'updated_at'
        )


class WalletCreateSerializer(WalletListSerializer):

    class Meta(WalletListSerializer.Meta):
        fields = ('id', 'title', 'description')


class WalletUpdateSerializer(WalletCreateSerializer):
    description = serializers.CharField(required=True)

    def validate(self, attrs):
        valid_update_wallet_title_and_description(self.instance, attrs)
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        wallet_id = instance.id
        title = validated_data.get('title')
        description = validated_data.get('description')

        wallet = Wallet.objects.filter(id=wallet_id).update(
            title=title,
            description=description
        )

        validated_data['id'] = wallet_id
        return validated_data
