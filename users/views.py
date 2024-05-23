from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView
)

from users.forms import CustomUserCreationForm


User = get_user_model()


class UserCreateView(CreateView):

    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('main:index')


class ProfileDetailView(DetailView):

    model = User
    template_name = 'users/profile.html'
    pk_url_kwarg = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """
        Переопределяем get_object, чтобы получить пользователя по имени, а не по идентификатору.
        """
        username = self.kwargs.get(self.slug_url_kwarg)
        return get_object_or_404(User, username=username)
