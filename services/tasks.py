from celery import shared_task
from django.db import transaction

from services.utils import delete_wallet_cache
from wallet.models import Wallet


@shared_task(
    name='wallet_create_task',
    autoretry_for=(Exception,),
    default_retry_delay=60
)
@transaction.atomic
def wallet_create(owner_id, title, description):
    Wallet.objects.create(
        owner_id=owner_id,
        title=title,
        description=description
    )


@shared_task(
    name='wallet_update_task',
    autoretry_for=(Exception,),
    default_retry_delay=60
)
def wallet_update(owner_id, wallet_id, title, description):
    Wallet.objects.filter(id=wallet_id).update(
        title=title,
        description=description
    )
    delete_wallet_cache(wallet_id, owner_id)


@shared_task(
    name='wallet_transaction_task',
    autoretry_for=(Exception,),
    default_retry_delay=60
)
@transaction.atomic
def wallet_transaction(wallet_id, owner_id, balance, operation_type, amount):
    if operation_type == 'DEPOSIT':
        balance += amount
    elif operation_type == 'WITHDRAW':
        balance -= amount

    Wallet.objects.filter(id=wallet_id).update(balance=balance)
    delete_wallet_cache(wallet_id, owner_id)
