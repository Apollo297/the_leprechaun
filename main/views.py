from django.views.generic import TemplateView


class HomePage(TemplateView):
    """Главная страница проекта."""

    template_name = 'main/index.html'
