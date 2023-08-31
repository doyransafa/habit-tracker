from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Habit, HabitEntry
from .forms import HabitForm
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

# Create your views here.

class CreateHabitView(CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'create_habit.html'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

class HabitDetailView(DetailView):
    model = Habit
    template_name = 'habit_details.html'
    context_object_name = 'habit'

class HabitListView(ListView):
    model = Habit
    template_name = 'index.html'
    context_object_name = 'habit_list'


class DeleteHabitView(DeleteView):
    model = Habit
    template_name = 'habit_delete_confirmation.html'
    context_object_name = 'habit'

    success_url = reverse_lazy('habit_list')


class UpdateHabitView(UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'habit_update.html'

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()