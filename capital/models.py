from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Currency(models.Model):
    """Модель валюты."""

    title = models.CharField(
        'Валюта',
        max_length=settings.TRANSACTION_MAX_LENGTH
    )
    symbol = models.CharField(
        'Символ',
        max_length=10
    )

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.title


class CapitalType(models.Model):
    """Модель типа капитала."""

    title = models.CharField(
        'Тип капитала',
        max_length=settings.TRANSACTION_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'Тип капитала'
        verbose_name_plural = 'Типы капитала'

    def __str__(self):
        return self.title


class Savings(models.Model):
    """Модель видов сбережений."""

    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    total_amount = models.DecimalField(
        'Общая сумма',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    user = models.ForeignKey(
        User,
        related_name='savings',
        on_delete=models.CASCADE
    )
    capital_type = models.ForeignKey(
        CapitalType,
        related_name='savings',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Тип'
    )
    currency = models.ForeignKey(
        Currency,
        related_name='savings',
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )

    class Meta:
        verbose_name = 'Вид сбережений'
        verbose_name_plural = 'Виды сбережений'

    def __str__(self):
        return f'{self.type} - {self.total_amount}'


class CapitalsTransaction(models.Model):
    """Модель транзакции одного из видов сбережений."""

    TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Списание')
    ]

    REPEAT_CHOICES = [
        ('daily', 'Ежедневно'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
        ('none', 'Без повтора')
    ]

    type = models.CharField(
        'Тип операции',
        max_length=10,
        choices=TYPE_CHOICES
    )
    savings = models.ForeignKey(
        Savings,
        related_name='capital_transactions',
        on_delete=models.CASCADE,
        verbose_name='Сбережение'
    )
    repeat = models.CharField(
        'Повтор операции',
        max_length=10,
        choices=REPEAT_CHOICES,
        default='none'
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        'Сумма транзакции',
        max_digits=10,
        decimal_places=2
    )
    pub_date = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Транзакция сбережения'
        verbose_name_plural = 'Транзакции сбережений'

    def __str__(self):
        return (
            f'Операция {self.get_type_display()} - '
            f'{self.pub_date: %d-%m-%Y %H:%M}'
        )
