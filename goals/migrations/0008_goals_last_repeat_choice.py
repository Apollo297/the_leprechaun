# Generated by Django 3.2.16 on 2024-05-28 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0007_alter_goals_goal_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='goals',
            name='last_repeat_choice',
            field=models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно'), ('none', 'Без повтора')], default='none', max_length=20, verbose_name='Последний выбор повтора транзакции'),
        ),
    ]
