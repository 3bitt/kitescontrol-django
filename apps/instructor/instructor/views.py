from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class InstructorHomeView(TemplateView):
    template_name = 'instructor/instructor_home.html'