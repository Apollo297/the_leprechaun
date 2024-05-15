from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)
from django.db import models


User = get_user_model()


class GoalTransaction(models.Model):
    """Модель транзакции для цели."""

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

    goal = models.ForeignKey(
        'Goals',
        related_name='goal_transactions',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='goal_transactions',
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
        validators=[MinValueValidator(0.01)]
    )
    repeat = models.CharField(
        'Повтор операции',
        max_length=20,
        choices=REPEAT_CHOICES,
        default='none'
    )
    pub_date = models.DateTimeField(
        'Дата и время транзакции',
        auto_now_add=True,
        editable=False
    )

    class Meta:
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
        related_name='goals',
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
    goal_amount = models.PositiveIntegerField('Необходимая сумма')
    term = models.PositiveIntegerField(
        'Срок',
        # Срок исчисляется в месяцах
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
    currency = models.CharField(
        'Валюта',
        max_length=10
    )
    accumulated = models.PositiveIntegerField(
        'Накоплено',
        default=0
    )
    is_done = models.BooleanField(
        'Достигнута ли цель',
        default=False
    )
    pub_date = models.DateTimeField(
        'Дата и время постановки цели',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title
