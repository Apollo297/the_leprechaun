from django import forms

from capital.models import Capital


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
