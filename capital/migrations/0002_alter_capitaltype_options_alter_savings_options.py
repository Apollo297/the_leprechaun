# Generated by Django 4.2.13 on 2024-05-14 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('capital', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capitaltype',
            options={'verbose_name': 'тип капитала', 'verbose_name_plural': 'Типы капитала'},
        ),
        migrations.AlterModelOptions(
            name='savings',
            options={'verbose_name': 'вид сбережений', 'verbose_name_plural': 'Виды сбережений'},
        ),
    ]