from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView

from goals.models import Goals


class GoalMixin(LoginRequiredMixin):
    model = Goals

    def get_object(self):
        """
        Переопределение метода get_object для получения конкретной цели
        текущего пользователя по первичному ключу (pk).
        Returns:
            Goals: Объект цели, отфильтрованный по pk и текущему пользователю.
        Raises:
            Http404: Если объект не найден.
        """
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            Goals,
            pk=pk,
            user=user
        )


class GoalDeleteViewMixin(GoalMixin, DeleteView):
    """Миксин удаления."""

    template_name = 'goal/delete_goal_confirm.html'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        """
        Переопределение метода get_context_data для добавления объекта
        цели в контекст.
        Args:
            **kwargs: Дополнительные аргументы контекста.
        Returns:
            dict: Контекст данных для передачи в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context['goal'] = get_object_or_404(
            Goals,
            pk=self.kwargs['pk']
        )
        return context
