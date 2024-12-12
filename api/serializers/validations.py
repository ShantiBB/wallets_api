from rest_framework.exceptions import ValidationError


# Валидация кошелька
def valid_update_wallet_title_and_description(instance, attrs):
    cur_title = instance.get('title')
    title = attrs.get('title')
    cur_description = instance.get('description')
    description = attrs.get('description')

    if cur_title == title and cur_description == description:
        raise ValidationError('Требуется внести изменения.')

# Валидация транзакции
def valid_transaction_amount(instance, value):
    message = None
    wallet = instance.context['wallet']
    request_data = instance.context.get('request').data
    operation_type = request_data.get('operation_type')
    balance = wallet.get('balance')

    if value < 10:
        message = 'Сумма транзакции не может быть меньше 10.'
    elif value > 1_000_000:
        message = 'Сумма транзакции не может быть больше 1 000 000.'
    elif operation_type == 'WITHDRAW' and balance < value:
        message = 'Недостаточно средств.'

    if message:
        raise ValidationError(message)
    return value


def valid_transaction_operation_type(value):
    if value not in ('DEPOSIT', 'WITHDRAW'):
        message = 'Неверный формат операции.'
        raise ValidationError(message)
    return value
