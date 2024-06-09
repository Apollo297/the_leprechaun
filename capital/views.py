from typing import Any, Dict, List

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
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


class CapitalCreateView(
    LoginRequiredMixin,
    CreateView
):
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


class CapitalsListView(
    LoginRequiredMixin,
    ListView
):
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


class CapitalDeleteView(
    CapitalMixin,
    DeleteView
):
    """Удаление капитала."""

    template_name = 'capital/delete_capital_confirm.html'


class CapitalTransactionCreateView(
    LoginRequiredMixin,
    CreateView
):
    """Создание транзакции."""

    model = CapitalsTransaction
    form_class = CapitalTransactionForm
    template_name = 'capital/new_capital_transaction.html'
    success_url = reverse_lazy('capital:capitals_list')

    def get_initial(self) -> Dict[str, Any]:
        initial: Dict[str, Any] = super().get_initial()
        capital_id = self.kwargs.get('pk')
        if capital_id:
            initial['capital'] = get_object_or_404(
                Capital,
                pk=capital_id
            )
        return initial

    def form_valid(self, form) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.currency = form.instance.capital.currency
        return super().form_valid(form)


class CapitalTransactionsListView(
    LoginRequiredMixin,
    ListView
):
    """Список транзакций конкретного типа капитала."""

    model = CapitalsTransaction
    paginate_by = settings.TRANSACTIONS_PAGE_PAGINATOR
    template_name = 'capital/capital_transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        """Фильтруем транзакции по выбранному капиталу."""
        capital_id: int = self.kwargs.get('pk')
        capital = get_object_or_404(
            Capital,
            pk=capital_id
        )
        queryset = CapitalsTransaction.objects.filter(capital=capital)
        start_date: str | None = self.request.GET.get('start_date')
        end_date: str | None = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date]
            )
        elif start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        elif end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Добавляем капитал в контекст."""
        context = super().get_context_data(**kwargs)
        capital_id: int = self.kwargs.get('pk')
        context['capital'] = get_object_or_404(
            Capital,
            pk=capital_id
        )
        return context

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any
    ) -> HttpResponse:
        if 'download' in request.GET:
            return self.download_transactions()
        return super().get(request, *args, **kwargs)

    def download_transactions(self):
        """Скачивание списка транзакций в формате txt."""
        capital_id = self.kwargs.get('pk')
        capital = get_object_or_404(Capital, pk=capital_id)
        transactions = CapitalsTransaction.objects.filter(
            capital=capital).order_by(
                '-created_at'
            )
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = (
            f'attachment; filename="transactions_list_{capital_id}.txt"'
        )
        response.write(
            f'Тип капитала: {capital.capital_type}: {capital.currency}\n\n'
        )
        date_width = 30
        type_width = 15
        amount_width = 10
        headers: List[str] = [
            "Дата".center(date_width),
            "Тип операции".center(type_width),
            "Сумма".center(amount_width)
        ]
        response.write("  ".join(headers) + "\n")
        for transaction in transactions:
            amount_str: str = (
                f'-{transaction.amount:.2f}'
                if transaction.type == 'withdrawal'
                else f'{transaction.amount:.2f}'
            )
            row: List[str] = [
                transaction.created_at.strftime(
                    "%d %B %Y, %H:%M"
                ).ljust(
                    date_width
                ),
                transaction.get_type_display().ljust(type_width),
                amount_str.center(amount_width)
            ]
            response.write("  ".join(row) + "\n")
        return response


class CapitalTransactionDetailView(
    LoginRequiredMixin,
    DetailView
):
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
