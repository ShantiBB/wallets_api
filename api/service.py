from django.db import transaction

from wallet.models import Wallet


@transaction.atomic
def update_balance(wallet, operation_type, amount):
    wallet_id = wallet.get('id')
    balance = wallet.get('balance')

    if operation_type == 'DEPOSIT':
        balance += amount
    elif operation_type == 'WITHDRAW':
        balance -= amount

    Wallet.objects.filter(id=wallet_id).update(balance=balance)
    return balance
