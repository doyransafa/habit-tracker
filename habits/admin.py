from django.contrib import admin

# Register your models here.
from .models import Habit, HabitEntry

admin.site.register((HabitEntry, Habit))