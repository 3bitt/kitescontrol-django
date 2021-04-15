from django.views.generic import TemplateView


class SearchHomeView(TemplateView):
    template_name = 'search/search_home.html'

