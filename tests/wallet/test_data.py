
def wallet_data_list():
    return (
        'id',
        'title',
        'balance',
        'owner',
    )


def wallet_data_retrieve():
    return (
        'id',
        'title',
        'description',
        'balance',
        'owner',
        'created_at',
        'updated_at'
    )


def wallet_data_create():
    return (
        'title',
        'description'
    )

