from django.shortcuts import render
from django.views import View
from account.views import UserAccessMixin
# Create your views here.


class HomeView(UserAccessMixin, View):
    permission_required = ''

    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/dashboard.html')
    
