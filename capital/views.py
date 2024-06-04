from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView
)
from django.urls import reverse_lazy

from capital.forms import (
    CapitalCreateForm,
    CapitalUpdateForm
)
from capital.models import Capital


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


class CapitalUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование цели."""

    model = Capital
    form_class = CapitalUpdateForm
    template_name = 'capital/update_capital.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('capital:capitals_list')

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            Capital,
            pk=pk,
            user=user
        )
