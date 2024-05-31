from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse_lazy

from capital.forms import CapitalsTransactionForm
from capital.models import CapitalsTransaction


class CapitalCreateView(LoginRequiredMixin, CreateView):
    """Создание новой транзакции."""

    model = CapitalsTransaction
    form_class = CapitalsTransactionForm
    template_name = 'capital/new_users_capital.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        """
        Переопределение метода form_valid для автоматического
        присвоения автора цели текущему пользователю.
        Args:
            form: Форма для создания новой цели.
        Returns:
            HttpResponse: Результат выполнения родительского метода form_valid.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        """
        Переопределение метода get_form_kwargs для передачи дополнительных
        аргументов в форму, в частности, текущего пользователя.
        Returns:
            dict: Аргументы, которые переданы в форму.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
