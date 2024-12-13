from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Wallet
from services.utils import delete_wallet_cache


@receiver(post_save, sender=Wallet)
def delete_wallet_cache_after_save(sender, instance, **kwargs):
    delete_wallet_cache(instance.id, instance.owner.id)


@receiver(post_delete, sender=Wallet)
def delete_wallet_cache_after_delete(sender, instance, **kwargs):
    delete_wallet_cache(instance.id, instance.owner.id)
