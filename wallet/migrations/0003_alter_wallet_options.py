# Generated by Django 5.1.4 on 2024-12-12 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0002_remove_wallet_operation_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wallet',
            options={'verbose_name': 'Список кошельков', 'verbose_name_plural': 'Кошельки'},
        ),
    ]