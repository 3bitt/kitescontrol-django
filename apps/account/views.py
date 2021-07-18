from django.contrib.auth.views import LoginView, redirect_to_login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from account.forms import RegisterForm
from account.models import User


class MainLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/'

class AccountCreateUserView(CreateView):
    template_name = 'account/account_create_user.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('crew_adm:crew-list')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AccountDetailUserView(DetailView):
    template_name = 'account/account_detail.html'
    queryset = User.objects.all()
    context_object_name = 'user'

class AccountEditUserView(UpdateView):
    template_name = 'account/account_update.html'
    model = User


