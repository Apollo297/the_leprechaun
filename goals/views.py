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


# добавить LoginRequiredMixin
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
        return reverse_lazy(
            'users:profile',
            kwargs={'username': self.request.user.username}
        )

    def get_form_kwargs(self):
        """
        Этот метод позволяет передать дополнительные аргументы в форму,
        в частности, текущего пользователя.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# PAGE_PAGINATOR = 10


# class CustomListMixin:
#     model = Post
#     paginate_by = PAGE_PAGINATOR

#     def get_queryset(self):
#         return (
#             Post.objects.select_related(
#                 'category', 'location', 'author'
#             ).annotate(
#                 comment_count=Count('comments')
#             )
#         ).order_by('-pub_date')


class GoalsListView(ListView):
    """Раздел целей."""

    model = Goals
    template_name = 'goal/goals_list.html'

    def get_queryset(self):
        return Goals.objects.all()

    # def get_queryset(self):
    #     return super().get_queryset().filter(
    #         is_published=True,
    #         category__is_published=True,
    #         pub_date__lte=timezone.now()
    #     )


class GoalDetailView(DetailView):
    model = Goals
    template_name = 'goal/goal_detail.html'
    context_object_name = 'goal'
