from django import forms

from capital.models import CapitalsTransaction


class CapitalsTransactionForm(forms.ModelForm):
    class Meta:
        model = CapitalsTransaction
        fields = (
            'capital_type',
            'type',
            'description',
            'amount',
            'currency'
        )

    def __init__(self, *args, **kwargs):
        super(CapitalsTransactionForm, self).__init__(*args, **kwargs)
