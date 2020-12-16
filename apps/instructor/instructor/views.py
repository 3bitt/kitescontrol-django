from django.views.generic.base import TemplateView
from django.views.generic import ListView, CreateView,DetailView,UpdateView,DeleteView
from .models import Instructor
from .forms import InstructorCreateForm
from django.urls import reverse_lazy
# Create your views here.

from account.models import UserManager
from account.models import User

class InstructorHomeView(TemplateView):
    template_name = 'instructor/instructor_home.html'

class InstructorListView(ListView):
    queryset = Instructor.objects.all().order_by('-register_date')
    context_object_name = 'instructor_list'
    template_name = 'instructor/instructor_list.html'

class InstructorCreateView(CreateView):
    model = Instructor
    template_name = 'instructor/instructor_create.html'
    form_class = InstructorCreateForm
    success_url = reverse_lazy('instructor:instructor-list')

    def form_valid(self, form):
        email = self.request.POST['email_address']
        user = User.objects.create_user(email=email, password=User.objects.make_random_password(length=20))

        self.model.user = user

        return super(InstructorCreateView, self).form_valid(form)

    # This can be done also in models.py (override save method)
    # def form_valid(self, request, *args, **kwargs):

    #     # name = self.request.POST['name']
    #     # name2 = self.request.POST['surname']

    #     # name = name[0].lower()
    #     # surname = name2.lower()
    #     # res = name + surname

    #     # UserManager.create_user(res, 'Password@1')
    #     a = User.objects.filter(username='gasdgas').first()
    #     print(a)
    #     return super().post(request, *args, **kwargs)



class InstructorDetailView(DetailView):
    queryset = Instructor.objects.all()
    template_name = 'instructor/instructor_detail.html'
    context_object_name = 'instructor'
    editMode = False


class InstructorUpdateView(UpdateView):
    model = Instructor
    template_name = 'instructor/instructor_detail.html'
    editMode = False
    form_class = InstructorCreateForm

    def get_success_url(self):
        return reverse_lazy('instructor:instructor-detail', kwargs={'pk': self.kwargs['pk']})

class InstructorDeleteView(DeleteView):
    model = Instructor
    success_url = reverse_lazy('instructor:instructor-list')
