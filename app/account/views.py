from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse, reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from account.forms import CustomAuthenticationForm, RegisterForm
from account.models import User


class MainLoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/'
    form_class = CustomAuthenticationForm


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


class AccountUpdateUserView(UpdateView):
    template_name = 'account/account_update.html'
    model = User
    fields = ['name', 'surname', 'email']
    context_object_name = 'user'

    def get_success_url(self) -> str:
        return reverse('account:detail-user', args=[self.object.id])


class AccountDeleteUserView(DeleteView):
    model = User
    success_url = reverse_lazy('crew_adm:crew-list')


class AccountChangeActiveStatus(RedirectView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('account:detail-user', args=[user_id]))
