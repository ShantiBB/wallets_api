from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from wallet.models import Wallet
from api.permissions import IsAuthorOrAdmin
from services.utils import check_response_cache
from api.serializers import (
    WalletListSerializer,
    WalletDetailSerializer,
    WalletCreateSerializer,
    WalletUpdateSerializer,
    TransactionCreateSerializer
)
from core.constants import (
    WALLET_LIST_FIELD,
    WALLET_RETRIEVE_FIELD,
    WALLET_UPDATE_FIELD,
    WALLET_TRANSACTION_FIELD,
    WALLET_OWNER_FIELD
)


class WalletViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (IsAuthorOrAdmin,)

    def get_queryset(self):
        user = self.request.user
        queryset = Wallet.objects.filter(owner=user).select_related('owner')

        if self.action == 'list':
            queryset = queryset.only(*WALLET_LIST_FIELD, *WALLET_OWNER_FIELD)
        elif self.action == 'retrieve':
            all_fields = (*WALLET_RETRIEVE_FIELD, *WALLET_OWNER_FIELD)
            queryset = queryset.only(*all_fields)
        elif self.action == 'update':
            queryset = queryset.only(*WALLET_UPDATE_FIELD)
        elif self.action == 'operation':
            queryset = queryset.only(*WALLET_TRANSACTION_FIELD)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return WalletListSerializer
        elif self.action == 'retrieve':
            return WalletDetailSerializer
        elif self.action == 'update':
            return WalletUpdateSerializer
        elif self.action == 'operation':
            return TransactionCreateSerializer
        return WalletCreateSerializer

    def list(self, request, *args, **kwargs):
        cache_key = f'wallet_list_{request.user.id}'
        return check_response_cache(self, request, cache_key, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        account_id = kwargs.get('pk')
        cache_key = f'wallet_{account_id}'
        return check_response_cache(self, request, cache_key, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=('post',), url_path='operation')
    def operation(self, request, pk=None):
        wallet = self.get_object()
        context = {'request': request, 'wallet': wallet}
        serializer = self.get_serializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'status': 'Успешно'},
            status=status.HTTP_201_CREATED
        )
