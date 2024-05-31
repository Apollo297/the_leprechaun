from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import CreateView
from django.urls import reverse_lazy

from capital.forms import CapitalsTransactionForm
from capital.models import (
    CapitalsTransaction,
    Savings
)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """Создание транзакции к типу капитала."""

    model = CapitalsTransaction
    form_class = CapitalsTransactionForm
    template_name = 'capital/new_users_capital.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """
        Назначаем текущего пользователя объекту формы перед его сохранением.
        Также проверяем наличие записи в модели Savings с указанным
        типом капитала. Если такой записи нет, она создаётся.
        Args:
            form (ModelForm): Объект формы, успешно прошедший валидацию.
        Returns:
            HttpResponse
        """
        form.instance.user = self.request.user
        capital_type = form.cleaned_data['capital_type']
        _, _ = Savings.objects.get_or_create(
            user=self.request.user,
            capital_type=capital_type
        )
        return super().form_valid(form)
