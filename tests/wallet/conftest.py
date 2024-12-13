import pytest
from celery import Celery
from django.conf import settings
from rest_framework.test import APIClient

from wallet.models import Wallet


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'memory://',
        'result_backend': 'rpc'
    }


@pytest.fixture
def api_client_owner():
    return APIClient()


@pytest.fixture
def api_client_not_owner():
    return APIClient()


@pytest.fixture
def api_client_anon():
    return APIClient()


@pytest.fixture
def owner_user(django_user_model):
    user = django_user_model.objects.create(
        username='owner',
        email='owner@test.ru',
        first_name='owner',
        last_name='owner',
        password='986svdscjkl23'
    )
    return user


@pytest.fixture
def not_owner_user(django_user_model):
    user = django_user_model.objects.create(
        username='not_owner',
        email='not_owner@test.ru',
        first_name='not_owner',
        last_name='not_owner',
        password='2rh39g8302f3'
    )
    return user


@pytest.fixture
def owner_auth(api_client_owner, owner_user):
    api_client_owner.force_authenticate(user=owner_user)
    return api_client_owner


@pytest.fixture
def not_owner_auth(api_client_not_owner, not_owner_user):
    api_client_not_owner.force_authenticate(user=not_owner_user)
    return api_client_not_owner


@pytest.fixture
def wallet(owner_user):
    wallet = Wallet.objects.create(
        owner_id=owner_user.id,
        title='Test wallet',
        description='Test wallet description'
    )
    return wallet

@pytest.fixture
def wallet_2(not_owner_user):
    wallet = Wallet.objects.create(
        owner_id=not_owner_user.id,
        title='Test wallet 2',
        description='Test wallet 2 description'
    )
    return wallet
