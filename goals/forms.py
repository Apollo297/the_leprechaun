from django import forms

from goals.models import (
    Goals,
    GoalTransaction
)


class GoalForm(forms.ModelForm):
    """Форма добавления цели."""

    class Meta:
        model = Goals
        exclude = (
            'user',
            'accumulated',
            'created_at'
        )

    def __init__(self, *args: object, **kwargs: dict[str, object]) -> None:
        """
        Добавляем возможность при инициализации формы передать объект
        пользователя через аргументы kwargs.
        Это позволит проверить уникальность
        целей не глобально, а только для данного пользователя.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self) -> str:
        title: str = self.cleaned_data['title']
        if Goals.objects.filter(title=title, user=self.user).exists():
            raise forms.ValidationError(
                'Цель с таким названием уже существует.'
            )
        return title


class GoalTransactionForm(forms.ModelForm):
    """Форма совершения транзакции цели."""

    class Meta:
        model = GoalTransaction
        fields = (
            'goal',
            'type',
            'transaction_amount',
        )

    def clean(self) -> dict[str, object]:
        cleaned_data: dict[str, object] = super().clean()
        transaction_type: str | None = cleaned_data.get('type')
        transaction_amount: int | None = cleaned_data.get('transaction_amount')
        goal = cleaned_data.get('goal')
        if (
            transaction_type == 'withdrawal' and
            transaction_amount > goal.accumulated
        ):
            raise forms.ValidationError(
                'Сумма списания не может превышать доступную сумму.'
            )
        elif (
            transaction_type == 'deposit' and
            transaction_amount > goal.goal_amount
        ):
            raise forms.ValidationError(
                'Сумма пополнения не может превышать '
                'установленную для накопления сумму.'
            )
        return cleaned_data
