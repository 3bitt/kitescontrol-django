from django.contrib.auth.decorators import login_required
from django.urls.conf import path
from crew.crew_adm.views import (
    CrewCreatePersonView,
    CrewCreateUserInstructorAjaxView,
    CrewListView,
)


app_name = 'crew_adm'
urlpatterns = [
    path('list/', login_required(CrewListView.as_view()), name='crew-list'),
    path(
        'create/',
        login_required(CrewCreatePersonView.as_view()),
        name='crew-create-person',
    ),
    path(
        'create/create-user-instructor/',
        login_required(CrewCreateUserInstructorAjaxView.as_view()),
        name='crew-create-user-instructor',
    ),
]
