from rest_framework import serializers
from djoser.serializers import UserSerializer

from services.tasks import wallet_create, wallet_update
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

    def create(self, validated_data):
        title = validated_data.get('title')
        description = validated_data.get('description')
        owner = validated_data.get('owner')
        wallet_create.delay(owner.id, title, description)
        return validated_data

    class Meta(WalletListSerializer.Meta):
        fields = ('id', 'title', 'description')


class WalletUpdateSerializer(WalletCreateSerializer):
    description = serializers.CharField(required=True)

    def validate(self, attrs):
        valid_update_wallet_title_and_description(self.instance, attrs)
        return attrs

    def update(self, instance, validated_data):
        owner_id = instance.owner.id
        wallet_id = instance.id
        title = validated_data.get('title')
        description = validated_data.get('description')

        wallet_update.delay(owner_id, wallet_id, title, description)

        validated_data['id'] = wallet_id
        return validated_data
