from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Writer
from django.contrib import messages
from .forms import UserRegistrationForm


class Home(TemplateView):
    template_name = 'home/home.html'


class About(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        username = kwargs['username']
        return super().get_context_data(**kwargs)


class UserRegistrationView(View):
    form_class = UserRegistrationForm
    template_name = 'home/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            messages.success(request, 'You registered successfully')
            return redirect('home:home')
        return render(request, self.template_name, context={'form': form})


class WritersView(LoginRequiredMixin, View):
    def get(self, request):
        writers = Writer.objects.all()
        return render(request, 'home/writers.html', {'writers': writers})
