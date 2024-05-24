# Generated by Django 4.2.13 on 2024-05-22 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('capital', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitalstransaction',
            name='savings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_capital_transactions', to='capital.savings', verbose_name='Сбережение'),
        ),
        migrations.AlterField(
            model_name='capitalstransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_capital_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='capital_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_type', to='capital.capitaltype', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_currency', to='capital.currency', verbose_name='Валюта'),
        ),
        migrations.AlterField(
            model_name='savings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_savings', to=settings.AUTH_USER_MODEL),
        ),
    ]