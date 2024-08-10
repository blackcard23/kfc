from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from log.forms import RegisterForm, LogForm


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'auth/register.html'

    def get_success_url(self):
        return reverse_lazy('main')
