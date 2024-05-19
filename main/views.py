from django.shortcuts import render

from django.views.generic import TemplateView


class IndexHome(TemplateView):
    template_name = 'main/index.html'
