from django import forms

from capital.models import (
    Capital,
    CapitalsTransaction
)


class CapitalCreateForm(forms.ModelForm):
    """Форма создания капитала для пользователя."""

    class Meta:
        model = Capital
        fields = (
            'capital_type',
            'currency',
            'description',
        )

    def __init__(self, *args: object, **kwargs: dict[str, object]) -> None:
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Проверка уникальности капитала и валюты для пользователя.
        """
        cleaned_data = super().clean()
        capital_type = cleaned_data.get('capital_type')
        currency = cleaned_data.get('currency')
        if self.user and Capital.objects.filter(
            capital_type=capital_type,
            currency=currency,
            user=self.user
        ).exists():
            raise forms.ValidationError(
                'У вас уже существует такой тип капитала с данной валютой.'
            )
        return cleaned_data


class CapitalUpdateForm(forms.ModelForm):
    """Форма изменения информации о капитале."""

    class Meta:
        model = Capital
        fields = ('description',)


class CapitalTransactionForm(forms.ModelForm):
    """Форма транзакции типа капитала."""

    class Meta:
        model = CapitalsTransaction
        fields = (
            'capital',
            'type',
            'description',
            'amount',
        )

    def clean(self) -> dict[str, object]:
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        transaction_amount = cleaned_data.get('amount')
        capital = cleaned_data.get('capital')
        if (
            transaction_type == 'withdrawal' and
            transaction_amount > capital.total_amount
        ):
            raise forms.ValidationError(
                'Сумма списания не может превышать доступную сумму.'
            )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.currency = self.cleaned_data['capital'].currency
        if commit:
            instance.save()
        return instance
