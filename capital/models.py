from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Currency(models.Model):
    """Модель валюты."""

    title = models.CharField(
        'Валюта',
        max_length=settings.TRANSACTION_MAX_LENGTH,
    )
    symbol = models.CharField(
        'Символ',
        max_length=10
    )

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Типы валют'

    def __str__(self):
        return f'{self.title} ({self.symbol})'


class CapitalType(models.Model):
    """Модель типа капитала."""

    title = models.CharField(
        'Тип капитала',
        max_length=settings.TRANSACTION_MAX_LENGTH
    )

    class Meta:
        verbose_name = 'тип капитала'
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
        related_name='user_savings',
        on_delete=models.CASCADE
    )
    capital_type = models.ForeignKey(
        CapitalType,
        related_name='savings_type',
        on_delete=models.CASCADE,
        null=False,
        verbose_name='Тип',
    )
    currency = models.ForeignKey(
        Currency,
        related_name='savings_currency',
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )

    class Meta:
        verbose_name = 'вид сбережений пользователя'
        verbose_name_plural = 'Виды сбережений пользователя'

    def __str__(self):
        return (
            f'{self.capital_type} - {self.total_amount} '
            f'{self.currency.symbol}'
        )


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
        choices=TYPE_CHOICES,
    )
    user = models.ForeignKey(
        User,
        related_name='user_capital_transactions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    savings = models.ForeignKey(
        Savings,
        related_name='savings_capital_transactions',
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
        verbose_name='Валюта',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Необязательное поле'
    )
    amount = models.DecimalField(
        'Сумма транзакции',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Транзакция сбережения'
        verbose_name_plural = 'Транзакции сбережений'

    def __str__(self):
        return (
            f'Операция {self.get_type_display()} - '
            f'{self.pub_date: %d-%m-%Y %H:%M}'
        )
