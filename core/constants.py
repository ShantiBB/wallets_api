FORMAT = '%d.%m.%Y %H:%M'

# Кошелёк
WALLET_LIST_FIELD = (
    'id',
    'title',
    'balance'

)
WALLET_RETRIEVE_FIELD = (
    'id',
    'title',
    'description',
    'balance',
    'created_at',
    'updated_at'
)

WALLET_UPDATE_FIELD = (
    'id',
    'title',
    'description',
    'owner__id'
)

WALLET_TRANSACTION_FIELD = (
    'id',
    'balance',
    'owner__id'
)

WALLET_OWNER_FIELD = (
    'owner__username',
    'owner__email',
    'owner__first_name',
    'owner__last_name',
    'owner__id'
)
