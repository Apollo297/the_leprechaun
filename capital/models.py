from decimal import Decimal

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
        return f'{self.title} ({self.symbol})'


class CapitalType(models.Model):
    """Модель типа капитала."""

    title = models.CharField(
        'Тип капитала',
        max_length=settings.TRANSACTION_MAX_LENGTH
    )
    currencies = models.ManyToManyField(
        Currency,
        verbose_name='Доступные валюты',
        related_name='capital_types'
    )

    class Meta:
        verbose_name = 'Тип капитала'
        verbose_name_plural = 'Типы капитала'

    def __str__(self):
        return self.title


class Savings(models.Model):
    """
    Модель для хранения информации о конкретных видах
    сбережений пользователя.
    """

    user = models.ForeignKey(
        User,
        related_name='user_savings',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    capital_type = models.ForeignKey(
        CapitalType,
        related_name='capital_type_savings',
        on_delete=models.CASCADE,
        verbose_name='Тип капитала'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Сбережения'
        verbose_name_plural = 'Сбережения'

    @property
    def total_amount(self):
        return sum(
            transaction.amount if transaction.type == 'deposit'
            else -transaction.amount
            for transaction in self.transactions.all()
        )

    def __str__(self):
        return f'{self.user} - {self.capital_type} - {self.total_amount}'


class CapitalsTransaction(models.Model):
    """Модель транзакции капиталов."""

    TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Списание')
    ]

    capital_type = models.ForeignKey(
        CapitalType,
        related_name='transaction_capital_type',
        on_delete=models.CASCADE,
        verbose_name='Тип капитала'
    )
    type = models.CharField(
        'Тип операции',
        max_length=10,
        choices=TYPE_CHOICES
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        'Сумма транзакции',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_transactions'
    )
    created_at = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Транзакция сбережения'
        verbose_name_plural = 'Транзакции сбережений'

    def __str__(self):
        return f'{self.user} - {self.type} - {self.amount}'
