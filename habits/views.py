
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Habit, HabitEntry
from .forms import HabitForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime, date


months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


class CreateHabitView(CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'create_habit.html'

    def form_valid(self, form):

        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()


class HabitDetailView(DetailView):
    model = Habit
    template_name = 'habit_details.html'
    context_object_name = 'habit'

    def get_object(self, queryset=None):
        habit = super().get_object(queryset)

        if habit.user != self.request.user:
            raise Http404("You don't have permission to access this habit.")

        return habit
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = date.today()
        month = today.month

        user_habits = Habit.objects.all().filter(user = self.request.user)

        context['today'] = today
        context['month'] = month
        context['months'] = months
        context['user_habits'] = user_habits
        context['active_habit_id'] = self.object.id

        return context

class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'index.html'
    context_object_name = 'habit_list'
    login_url = "auth/login"

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class DeleteHabitView(DeleteView):
    model = Habit
    template_name = 'habit_delete_confirmation.html'
    context_object_name = 'habit'

    success_url = reverse_lazy('habit_list')

    def get_object(self, queryset=None):
        habit = super().get_object(queryset)

        if habit.user != self.request.user:
            raise Http404("You don't have permission to access this habit.")

        return habit


class UpdateHabitView(UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habit_update.html'

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()
    
    def get_object(self, queryset=None):
        habit = super().get_object(queryset)

        if habit.user != self.request.user:
            raise Http404("You don't have permission to access this habit.")

        return habit


def date_toggle(request, habit_id, date, quantity=1):

    habit = Habit.objects.get(pk=habit_id)

    if habit.user != request.user:
        raise Http404("You don't have permission to access this habit.")

    entry_date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    if HabitEntry.objects.filter(habit=habit, entry_date=entry_date_obj).exists():
        HabitEntry.objects.filter(habit=habit, entry_date=entry_date_obj).delete()
    else: 
        HabitEntry.objects.create(habit=habit, entry_date=entry_date_obj, quantity=quantity)

    return redirect('habit_details', pk=habit_id)
