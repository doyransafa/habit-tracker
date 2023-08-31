from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages

# Create your views here.


class CustomLoginView(LoginView):
    def get_success_url(self):
        return '/'

    def form_valid(self, form):
        messages.success(self.request, "You have been successfully logged in.")
        return super().form_valid(form)
