from django.http import Http404
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Habit, HabitEntry
from django.contrib.auth.models import User
from .forms import HabitForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from calendar import Calendar
from datetime import datetime

# Create your views here.


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

class HabitListView(LoginRequiredMixin,ListView):
    model = Habit
    template_name = 'index.html'
    context_object_name = 'habit_list'

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


def date_toggle(request, habit_id, date):

    habit = Habit.objects.get(pk=habit_id)

    entry_date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    _, created = HabitEntry.objects.get_or_create(habit=habit, entry_date = entry_date_obj)

    if not created:
        habit.habitentry_set.filter(entry_date = date).delete()

    return redirect('habit_details', pk=habit_id)
