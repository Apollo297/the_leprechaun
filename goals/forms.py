from django import forms

from goals.models import (
    Goals,
    GoalTransaction
)


class GoalForm(forms.ModelForm):
    """Форма добавления цели."""
    
    # Сделать валидацию в форму на уникальность цели
    # def clean(self):
    #     super().clean()
    #     title = self.cleaned_data['title']
    #     if title in ...
    
    class Meta:
        model = Goals
        exclude = (
            'user',
            'accumulated',
            'is_done',
            'pub_data'
        )


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
