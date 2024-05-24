from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView
)

from goals.models import Goals
from users.forms import (
    CustomUserCreationForm,
    CustomUserUpdateForm
)


User = get_user_model()


class UserCreateView(CreateView):
    """Регистрация пользователя."""

    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('main:index')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """Профиль пользователя."""

    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        context['recent_goals'] = Goals.objects.filter(
            user=self.request.user
            ).order_by(
                '-created_at'
            )[:5]
        return context

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля."""

    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('users:profile')
