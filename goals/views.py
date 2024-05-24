# from django.contrib.auth.mixins import LoginRequiredMixin
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

PAGE_PAGINATOR = 5


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


class GoalsListView(ListView):
    """Раздел целей."""

    model = Goals
    paginate_by = PAGE_PAGINATOR
    template_name = 'goal/goals_list.html'

    def get_queryset(self):
        return Goals.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_goals'] = Goals.objects.all().order_by(
            '-created_at'
        )[:5]
        return context


class GoalDetailView(DetailView):
    model = Goals
    template_name = 'goal/goal_detail.html'
    context_object_name = 'goal'
