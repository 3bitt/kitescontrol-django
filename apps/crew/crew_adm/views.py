from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView
from django.db.models.query_utils import Q
from account.forms import RegisterForm

from account.models import User
from crew.instructor.forms import InstructorCreateForm
from crew.instructor.models import Instructor
# Create your views here.


class CrewListView(ListView):
    template_name = 'crew_adm/crew_list.html'
    queryset = User.objects.filter(~Q(type='ADMIN')).order_by('-created_date')
    context_object_name = 'all_users'

    def get_context_data(self, **kwargs):
        context_data_dict = super().get_context_data(**kwargs)
        context_data_dict['manager_users'] = context_data_dict['all_users'].filter(
            type='MANAGER')
        context_data_dict['clerk_users'] = context_data_dict['all_users'].filter(
            type='CLERK')
        context_data_dict['instructor_users'] = context_data_dict['all_users'].filter(
            type='INSTRUCTOR')
        return context_data_dict


class CrewCreatePersonView(TemplateView):
    template_name = 'crew_adm/crew_create_person.html'
    form_class = RegisterForm


class CrewCreateUserInstructorAjaxView(CreateView):
    model = Instructor
    template_name = 'instructor/instructor_create.html'
    form_class = InstructorCreateForm


class CrewCreateUserView(CreateView):
    pass
