from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'pages/about.html'


def csrf_failure(request, reason=''):
    """Обработка ошибки 403."""
    return render(request, 'pages/403csrf.html', status=403)
