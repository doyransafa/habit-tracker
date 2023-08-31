from django.urls import reverse
from django.db import models

# Create your models here.

class User(models.Model):
    ...

class Habit(models.Model):

    UNIT_CHOICES = (('time', 'Time (minutes)'), ('repetition',
                    'Repetition'), ('distance', 'Distance (km)'), ('check', 'Check'))

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    created_at = models.DateField(auto_now_add=True)
    units = models.CharField(max_length=50, choices=UNIT_CHOICES)
    goal = models.PositiveIntegerField()
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("habit_details", kwargs={"pk": self.pk})
    

class HabitEntry(models.Model):

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    entry_date = models.DateField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.habit.name} - {self.entry_date}'
    
