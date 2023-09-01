from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.


class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        messages.success(self.request, "You have been successfully logged in.")
        return super().form_valid(form)

class RegistrationView(FormView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('habit_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    