from django import forms

from capital.models import CapitalsTransaction


class CapitalsTransactionForm(forms.ModelForm):
    """Форма добавления средств в накопления."""

    class Meta:
        model = CapitalsTransaction
        exclude = (
            'user',
            'pub_data'
        )
