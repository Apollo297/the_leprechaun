from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse_lazy

from goals.forms import GoalForm
from goals.models import Goals

PAGE_PAGINATOR = 10


class GoalCreateView(CreateView):
    """Создание новой цели накоплений."""

    model = Goals
    form_class = GoalForm
    template_name = 'goal/new_goal.html'

    def form_valid(self, form):
        """
        При создании поста мы не можем указывать автора вручную,
        для этого переопределим метод валидации:
        Args:
            form: Форма для валидации
        Returns:
            Результат родительского метода form_valid.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('users:profile')

    def get_form_kwargs(self):
        """
        Этот метод позволяет передать дополнительные аргументы в форму,
        в частности, текущего пользователя.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GoalsListView(LoginRequiredMixin, ListView):
    """Раздел целей."""

    model = Goals
    paginate_by = PAGE_PAGINATOR
    template_name = 'goal/goals_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goals.objects.filter(
            user=self.request.user
            ).order_by(
                '-created_at'
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_goals'] = Goals.objects.filter(
            user=self.request.user
            ).order_by(
                '-created_at'
            )
        return context


class GoalDetailView(LoginRequiredMixin, DetailView):
    """Детальная информация о цели."""

    model = Goals
    template_name = 'goal/goal_detail.html'
    context_object_name = 'goal'

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            Goals,
            pk=pk,
            user=user
        )


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование цели."""

    model = Goals
    form_class = GoalForm
    template_name = 'goal/new_goal.html'
    pk_url_kwarg = 'pk'

    def get_queryset(self):
        """
        Ограничивает доступ к целям текущего пользователя.
        """
        return super().get_queryset().filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        goal = self.get_object()
        if goal.user != self.request.user:
            raise Http404("Цель не найдена.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('goals:goal_detail', args=[self.kwargs['pk']])


class GoalDeleteView(DeleteView):
    pass
