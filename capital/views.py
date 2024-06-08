from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)
from django.urls import reverse_lazy

from capital.forms import (
    CapitalCreateForm,
    CapitalTransactionForm,
    CapitalUpdateForm
)
from capital.mixins import CapitalMixin
from capital.models import (
    Capital,
    CapitalsTransaction
)


class CapitalCreateView(LoginRequiredMixin, CreateView):
    """Создание типа капитала."""

    model = Capital
    form_class = CapitalCreateForm
    template_name = 'capital/create_capital.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CapitalsListView(LoginRequiredMixin, ListView):
    """Раздел капиталов."""

    model = Capital
    paginate_by = settings.PAGE_PAGINATOR
    template_name = 'capital/capitals_list.html'
    context_object_name = 'my_capitals'

    def get_queryset(self):
        return Capital.objects.filter(
            user=self.request.user
        )


class CapitalUpdateView(CapitalMixin, UpdateView):
    """Редактирование типа капитала."""

    form_class = CapitalUpdateForm
    template_name = 'capital/update_capital.html'


class CapitalDeleteView(CapitalMixin, DeleteView):
    """Удаление капитала."""

    template_name = 'capital/delete_capital_confirm.html'


class CapitalTransactionCreateView(LoginRequiredMixin, CreateView):
    """Создание транзакции цели накоплений."""

    model = CapitalsTransaction
    form_class = CapitalTransactionForm
    template_name = 'capital/new_capital_transaction.html'
    success_url = reverse_lazy('capital:capitals_list')

    def get_initial(self):
        initial = super().get_initial()
        capital_id = self.kwargs.get('pk')
        if capital_id:
            initial['capital'] = get_object_or_404(
                Capital,
                pk=capital_id
            )
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = form.instance.capital.currency
        return super().form_valid(form)


class CapitalTransactionsListView(LoginRequiredMixin, ListView):
    """Список транзакций конкретной типа капитала."""

    model = CapitalsTransaction
    paginate_by = settings.PAGE_PAGINATOR
    template_name = 'capital/capital_transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        """Фильтруем транзакции по выбранному капиталу."""
        capital_id = self.kwargs.get('pk')
        capital = get_object_or_404(
            Capital,
            pk=capital_id
        )
        return CapitalsTransaction.objects.filter(
            capital=capital
            ).order_by(
                '-created_at'
        )

    def get_context_data(self, **kwargs):
        """Добавляем капитал в контекст."""
        context = super().get_context_data(**kwargs)
        capital_id = self.kwargs.get('pk')
        context['capital'] = get_object_or_404(
            Capital,
            pk=capital_id
        )
        return context


class CapitalTransactionDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о транзакции капитала."""

    model = CapitalsTransaction
    template_name = 'capital/detail_capital_transaction.html'
    context_object_name = 'transaction'

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            CapitalsTransaction,
            pk=pk,
            user=user
        )
