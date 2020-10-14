from django.shortcuts import render
from django.views.generic import View, TemplateView
# Create your views here.


class Index(TemplateView):
    template_name = 'main/base.html'
    