from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home/home.html'


class About(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        return super().get_context_data(**kwargs)
