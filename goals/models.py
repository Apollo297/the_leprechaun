from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models

from capital.models import Currency


User = get_user_model()


class GoalTransaction(models.Model):
    """Модель транзакции для цели."""

    TYPE_CHOICES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Списание')
    ]

    goal = models.ForeignKey(
        'Goals',
        related_name='goal_transactions',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='user_goal_transactions',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    type = models.CharField(
        'Тип операции',
        max_length=20,
        choices=TYPE_CHOICES
    )
    transaction_amount = models.DecimalField(
        'Сумма транзакции',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.ForeignKey(
        Currency,
        related_name='currency_goal_transactions',
        on_delete=models.CASCADE,
        verbose_name='Валюта',
    )
    created_at = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'транзакция для цели'
        verbose_name_plural = 'Транзакции для цели'

    def __str__(self):
        return (
            f'Операция {self.get_type_display()} - '
            f'{self.pub_date: %d-%m-%Y %H:%M}'
        )


class Goals(models.Model):
    """Модель поставленных целей."""

    user = models.ForeignKey(
        User,
        related_name='user_goals',
        on_delete=models.CASCADE
    )
    title = models.CharField(
        'Название',
        max_length=settings.CHAR_MAX_LENGTH,
        unique=True
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
        help_text='Необязательное поле'
    )
    goal_amount = models.DecimalField(
        'Необходимая сумма',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    term = models.PositiveIntegerField(
        'Срок',
        help_text='В месяцах',
        validators=[
            MinValueValidator(settings.MIN_VALUE),
            MaxValueValidator(settings.MAX_VALUE)
        ],
    )
    image = models.ImageField(
        'Изображение',
        upload_to='goal_images',
        blank=True,
        null=True
    )
    currency = models.ForeignKey(
        Currency,
        related_name='currency_goals',
        on_delete=models.CASCADE,
        verbose_name='Валюта'
    )
    accumulated = models.DecimalField(
        'Накоплено',
        max_digits=10,
        decimal_places=2,
        default=0
    )
    created_at = models.DateTimeField(
        'Дата и время постановки цели',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'цель'
        verbose_name_plural = 'Цели'
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'currency'),
                name='Unique goal constraint',
            ),
        )

    def remaining_amount(self):
        """
        Метод для вычисления оставшейся суммы до достижения цели.
        Returns:
            decimal.Decimal: Необходимая сумма для достижения цели,
            либо 0, если равно цели.
        """
        return max(0, self.goal_amount - self.accumulated)

    def is_completed(self):
        """
        Метод для проверки достижения цели.
        Returns:
            bool: True, если равно цели, иначе False.
        """
        return self.accumulated >= self.goal_amount

    def __str__(self):
        return self.title
