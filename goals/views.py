from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import (
    Q,
    F
)
from django.shortcuts import (
    get_object_or_404,
    redirect
)
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.urls import reverse_lazy

from goals.forms import (
    GoalForm,
    GoalTransactionForm
)
from goals.models import (
    Goals,
    GoalTransaction
)

PAGE_PAGINATOR = 10


class GoalCreateView(LoginRequiredMixin, CreateView):
    """Создание новой цели накоплений."""

    model = Goals
    form_class = GoalForm
    template_name = 'goal/new_goal.html'
    success_url = reverse_lazy('users:profile')

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
    template_name = 'goal/detail_goal.html'
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

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            Goals,
            pk=pk,
            user=user
        )

    def get_success_url(self):
        return reverse_lazy(
            'goals:detail_goal',
            args=[self.kwargs['pk']]
        )


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление цели."""

    model = Goals
    template_name = 'goal/delete_goal_confirm.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('goals:goals_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = get_object_or_404(
            Goals,
            pk=self.kwargs['pk']
        )
        return context

    def get_object(self):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(
            Goals,
            pk=pk,
            user=user
        )


class GoalTransactionCreateView(LoginRequiredMixin, CreateView):
    """Создание транзакции цели накоплений."""

    model = GoalTransaction
    form_class = GoalTransactionForm
    template_name = 'goal/new_goal_transaction.html'
    success_url = reverse_lazy('goals:goals_list')

    def get_initial(self):
        """Получение начальных данных формы для предварительного заполнения."""
        initial = super().get_initial()
        goal_id = self.kwargs.get('pk')
        if goal_id:
            initial['goal'] = get_object_or_404(Goals, pk=goal_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.currency = form.instance.goal.currency
        goal = form.instance.goal
        if form.instance.type == 'deposit':
            goal.accumulated += form.instance.transaction_amount
        elif form.instance.type == 'withdrawal':
            goal.accumulated -= form.instance.transaction_amount
        goal.save()
        if goal.is_completed():
            return redirect('goals:archive_goals')
        return super().form_valid(form)


class ArchiveGoalListView(LoginRequiredMixin, ListView):
    model = Goals
    template_name = 'goal/archive_goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goals.objects.filter(
            Q(user=self.request.user) & Q(accumulated__gte=F('goal_amount'))
        )
