from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

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
