from django.conf import settings
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
from goals.mixins import (
    GoalDeleteViewMixin,
    GoalMixin
)


class GoalCreateView(LoginRequiredMixin, CreateView):
    """Создание новой цели накоплений."""

    model = Goals
    form_class = GoalForm
    template_name = 'goal/new_goal.html'
    success_url = reverse_lazy('users:profile')

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


class GoalsListView(LoginRequiredMixin, ListView):
    """Раздел целей."""

    model = Goals
    paginate_by = settings.PAGE_PAGINATOR
    template_name = 'goal/goals_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        """
        Переопределение метода get_queryset для фильтрации целей по текущему
        пользователю и сортировка их по дате создания в порядке убывания.
        Returns:
            QuerySet
        """
        return Goals.objects.filter(
            user=self.request.user).order_by(
                '-created_at'
            )

    def get_context_data(self, **kwargs):
        """
        Переопределение метода get_context_data для добавления дополнительных
        данных в контекст шаблона.
        Args:
            **kwargs: Дополнительные аргументы контекста.
        Returns:
            dict: Контекст данных для передачи в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context['recent_goals'] = Goals.objects.filter(
            user=self.request.user).order_by(
                '-created_at'
            )
        return context


class GoalDetailView(GoalMixin, DetailView):
    """Детальная информация о цели."""

    template_name = 'goal/detail_goal.html'
    context_object_name = 'goal'


class GoalUpdateView(GoalMixin, UpdateView):
    """Редактирование цели."""

    form_class = GoalForm
    template_name = 'goal/new_goal.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        """
        Переопределение метода get_success_url для получения URL
        успешного редиректа после редактирования цели.
        Returns:
            str
        """
        return reverse_lazy(
            'goals:detail_goal',
            args=[self.kwargs['pk']]
        )


class GoalDeleteView(GoalDeleteViewMixin):
    """Удаление цели."""

    success_url = reverse_lazy('goals:goals_list')


class GoalTransactionCreateView(LoginRequiredMixin, CreateView):
    """Создание транзакции цели накоплений."""

    model = GoalTransaction
    form_class = GoalTransactionForm
    template_name = 'goal/new_goal_transaction.html'
    success_url = reverse_lazy('goals:goals_list')

    def get_initial(self):
        """
        Получение начальных данных формы для предварительного заполнения.
        Returns:
            dict
        """
        initial = super().get_initial()
        goal_id = self.kwargs.get('pk')
        if goal_id:
            initial['goal'] = get_object_or_404(
                Goals,
                pk=goal_id
            )
        return initial

    def form_valid(self, form):
        """
        Переопределение метода form_valid для обработки валидной формы и
        обновления цели в зависимости от типа транзакции.
        Args:
            form: Валидная форма транзакции.
        Returns:
            HttpResponseRedirect: Редирект на указанный URL.
        """
        form.instance.user = self.request.user
        form.instance.currency = form.instance.goal.currency
        goal = form.instance.goal
        response = super().form_valid(form)
        if form.instance.type == 'deposit':
            goal.accumulated += form.instance.transaction_amount
        elif form.instance.type == 'withdrawal':
            goal.accumulated -= form.instance.transaction_amount
        goal.save()
        if goal.is_completed():
            return redirect('goals:archive_goals')
        return response


class ArchiveGoalListView(LoginRequiredMixin, ListView):
    """
    Список архивированных целей накоплений, у которых достигнута
    целевая сумма.
    """

    model = Goals
    template_name = 'goal/archive_goal_list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        """
        Returns:
            QuerySet: Список архивированных целей.
        """
        return Goals.objects.filter(
            Q(user=self.request.user) & Q(accumulated__gte=F(
                'goal_amount'
            ))
        )


class GoalTransactionsListView(LoginRequiredMixin, ListView):
    """Список транзакций конкретной цели."""

    model = GoalTransaction
    paginate_by = settings.PAGE_PAGINATOR
    template_name = 'goal/goal_transactions_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        """
        Переопределение метода get_queryset для фильтрации транзакций
        по конкретной цели и их сортировка по дате создания в порядке убывания.
        Returns:
            QuerySet
        """
        self.goal = get_object_or_404(
            Goals,
            pk=self.kwargs['pk']
        )
        return GoalTransaction.objects.filter(
            goal=self.goal
            ).order_by(
                '-created_at'
        )

    def get_context_data(self, **kwargs):
        """Добавление цели в контекст шаблона ."""
        context = super().get_context_data(**kwargs)
        context['goal'] = self.goal
        return context


class ArchiveGoalDeleteView(GoalDeleteViewMixin):
    """Удаление цели из архива."""

    success_url = reverse_lazy('goals:archive_goals')
