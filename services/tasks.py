from celery import shared_task
from django.db import transaction

from services.utils import delete_wallet_cache
from wallet.models import Wallet


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
