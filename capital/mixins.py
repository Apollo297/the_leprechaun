from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from capital.models import Capital


class CapitalMixin(LoginRequiredMixin):
    """Миксин типа капитала."""

    model = Capital
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
