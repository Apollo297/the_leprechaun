# Generated by Django 4.2.13 on 2024-05-14 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capital', '0004_capitalstransaction_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'verbose_name': 'Валюта', 'verbose_name_plural': 'Типы валют'},
        ),
    ]