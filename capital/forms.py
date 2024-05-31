from django import forms

from capital.models import (
    CapitalsTransaction,
    Savings
)


# class CapitalsTransactionForm(forms.ModelForm):
#     """Форма добавления средств в накопления."""

#     class Meta:
#         model = CapitalsTransaction
#         fields = (
#             'transaction_type',
#             'description',
#             'amount',
#             'savings',
#             'currency'
#         )

#     def __init__(self, *args: object, **kwargs: dict[str, object]) -> None:
#         """
#         Добавляем возможность при инициализации формы передать объект
#         пользователя через аргументы kwargs.
#         """
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user:
#             self.fields['savings'].queryset = Savings.objects.filter(user=user)


class CapitalsTransactionForm(forms.ModelForm):
    """Форма добавления/списания средств из накоплений."""

    class Meta:
        model = CapitalsTransaction
        fields = (
            'transaction_type',
            'description',
            'amount',
            'savings',
            'currency'
        )

    def __init__(self, *args, **kwargs):
        """Добавляем возможность при инициализации формы передать объект пользователя через аргументы kwargs."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['savings'].queryset = Savings.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        savings = cleaned_data.get('savings')

        if transaction_type == 'withdrawal' and savings:
            if amount > savings.total_amount:
                raise forms.ValidationError('Сумма списания не может превышать общую сумму сбережений.')

        if savings and cleaned_data.get('currency') != savings.currency:
            raise forms.ValidationError('Валюта транзакции должна совпадать с валютой сбережений.')

        return cleaned_data

    def save(self, commit=True):
        transaction = super().save(commit=False)

        savings = transaction.savings
        if transaction.transaction_type == 'deposit':
            savings.total_amount += transaction.amount
        elif transaction.transaction_type == 'withdrawal':
            savings.total_amount -= transaction.amount

        if commit:
            savings.save()
            transaction.save()
        return transaction
