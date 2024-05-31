# Generated by Django 3.2.16 on 2024-05-31 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goals', '0001_initial'),
        ('capital', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='goaltransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_goal_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='goals',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='currency_goals', to='capital.currency', verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='goals',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_goals', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='goals',
            constraint=models.UniqueConstraint(fields=('title', 'currency'), name='Unique goal constraint'),
        ),
    ]
