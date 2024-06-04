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
        max_length=3,
    )
    symbol = models.CharField(
        'Символ',
        max_length=1
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

    class Meta:
        verbose_name = 'Тип капитала'
        verbose_name_plural = 'Типы капитала'

    def __str__(self):
        return self.title


class Capital(models.Model):
    """Модель капитала пользователя."""
    user = models.ForeignKey(
        User,
        related_name='capitals',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    capital_type = models.ForeignKey(
        CapitalType,
        related_name='capitals',
        on_delete=models.CASCADE,
        verbose_name='Тип капитала'
    )
    currency = models.ForeignKey(
        Currency,
        related_name='capitals',
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Капитал'
        verbose_name_plural = 'Капиталы'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'capital_type', 'currency'),
                name='unique_user_capital_type_currency'
            ),
        ]

    @property
    def total_amount(self):
        return sum(
            transaction.amount if transaction.type == 'deposit'
            else -transaction.amount
            for transaction in self.transactions.all()
        )

    def __str__(self):
        return (
            f'{self.user} - '
            f'{self.capital_type} - '
            f'{self.currency} - '
            f'{self.total_amount}'
        )


class CapitalsTransaction(models.Model):
    """Модель транзакции капиталов."""

    TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Списание')
    ]

    capital = models.ForeignKey(
        Capital,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name='Капитал'
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
        related_name='transactions',
        verbose_name='Валюта'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions',
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
        return f'{self.capital} - {self.type} - {self.amount}'
