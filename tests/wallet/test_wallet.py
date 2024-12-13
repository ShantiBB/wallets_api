import pytest
from django.contrib.auth import get_user_model
from pytest_lazyfixture import lazy_fixture
from django.urls import reverse
from rest_framework import status

from tests.wallet.test_data import (
    wallet_data_list,
    wallet_data_retrieve,
    wallet_data_create
)
from services.tasks import *

User = get_user_model()

@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    'user, status, check_own', (
        (lazy_fixture('owner_auth'), status.HTTP_200_OK, True),
        (lazy_fixture('not_owner_auth'), status.HTTP_200_OK, False),
        (lazy_fixture('api_client_anon'), status.HTTP_403_FORBIDDEN, False),
    )
)
def test_wallets_list(user, status, check_own, wallet):
    url = reverse('wallet-list')
    response = user.get(url)
    assert response.status_code == status
    if status == 200:
        if check_own:
            assert tuple(response.data[0]) == wallet_data_list()
        else:
            assert response.data == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status', (
        (lazy_fixture('owner_auth'), status.HTTP_200_OK),
        (lazy_fixture('not_owner_auth'), status.HTTP_404_NOT_FOUND),
        (lazy_fixture('api_client_anon'), status.HTTP_403_FORBIDDEN),
    )
)
def test_wallet_retrieve(user, status, wallet):
    url = reverse('wallet-detail', args=(wallet.id,))
    response = user.get(url)
    assert response.status_code == status
    if status == 200:
        assert tuple(response.data) == wallet_data_retrieve()


@pytest.mark.django_db(transaction=True)
def test_wallet_create(owner_user):
    assert Wallet.objects.count() == 0
    result = wallet_create(owner_user.id, 'test', 'test')
    assert Wallet.objects.count() == 1


@pytest.mark.django_db(transaction=True)
def test_wallet_update(owner_user, wallet):
    wallet_update(
        owner_user.id,
        wallet.id,
        'test',
        'test'
    )
    assert Wallet.objects.get(id=wallet.id).title == 'test'


@pytest.mark.django_db(transaction=True)
def test_transaction_create(owner_user, wallet):
    assert Wallet.objects.get(id=wallet.id).balance == 0
    wallet_transaction(
        wallet.id,
        owner_user.id,
        wallet.balance,
        'DEPOSIT',
        100
    )
    assert Wallet.objects.get(id=wallet.id).balance == 100
