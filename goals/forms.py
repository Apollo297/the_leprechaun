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
            'is_done',
            'pub_date'
        )

    def __init__(self, *args, **kwargs):
        # Добавляем возможность при инициализации формы передать объект
        # пользователя через аргументы kwargs.
        # Это позволит проверить уникальность
        # целей не глобально, а только для данного пользователя.
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Goals.objects.filter(title=title, user=self.user).exists():
            raise forms.ValidationError(
                'Цель с таким названием уже существует.'
            )
        return title


class GoalTransactionForm(forms.ModelForm):
    """Форма добавления средств к цели."""

    class Meta:
        model = GoalTransaction
        fields = (
            'goal',
            'type',
            'transaction_amount',
            'repeat'
        )
