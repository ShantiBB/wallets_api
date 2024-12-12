from functools import partial

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from wallet.models import Wallet
from api.serializers import (
    WalletSerializer,
    WalletCreateSerializer,
    WalletUpdateSerializer,
    TransactionCreateSerializer
)


class WalletViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_queryset(self):
        if self.action == 'update':
            return Wallet.objects.values('id', 'title', 'description')
        elif self.action == 'operation':
            return Wallet.objects.values(
                'id', 'balance'
            )
        return Wallet.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return WalletCreateSerializer
        elif self.action == 'update':
            return WalletUpdateSerializer
        elif self.action == 'operation':
            return TransactionCreateSerializer
        return WalletSerializer

    def perform_update(self, serializer):
        serializer.save(partial=True)

    @action(detail=True, methods=('post',), url_path='operation')
    def operation(self, request, pk=None):
        wallet = self.get_object()
        context = {'request': request, 'wallet': wallet}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
