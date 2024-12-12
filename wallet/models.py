import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Wallet(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(
        max_length=50,
        verbose_name='Название кошелька'
    )
    description = models.TextField(
        null=True, blank=True,
        verbose_name='Описание кошелька'
    )
    balance = models.DecimalField(
        default=0,
        max_digits=9,
        decimal_places=2,
        verbose_name='Баланс',
        validators=(
            MinValueValidator(0),
            MaxValueValidator(1_000_000)
        )
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего обновления'
    )

    class Meta:
        verbose_name = 'Кошелёк'
        verbose_name_plural = "Список кошельков"
        ordering = ['created_at']

    def __str__(self):
        return self.title
