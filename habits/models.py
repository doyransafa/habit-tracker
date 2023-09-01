from calendar import Calendar
from datetime import date, timedelta, datetime
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Habit(models.Model):

    UNIT_CHOICES = (('time', 'Time (minutes)'), ('repetition',
                    'Repetition'), ('distance', 'Distance (km)'), ('check', 'Check'))

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    created_at = models.DateField(auto_now_add=True)
    units = models.CharField(max_length=50, choices=UNIT_CHOICES)
    goal = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("habit_details", kwargs={"pk": self.pk})
    
    def get_entry_dates(self):
        datetime_list = self.habitentry_set.values_list('entry_date', flat=True).order_by('-entry_date')
        return datetime_list
    
    def get_year_list(self):
        calendar = Calendar()
        whole_year = []
        for month in range(1,13):
            days = calendar.itermonthdates(2023, month)
            day_list = [day for day in days]
            days = [day for day in day_list if day.month == month]
            whole_year.append(days)

        return whole_year    

    def get_current_streak(self):
        today = date.today()
        entry_dates = self.get_entry_dates()

        current_streak = 0
        if today not in entry_dates:
            return current_streak
        else:
            for i, entry in enumerate(entry_dates):
                if (today - entry).days == i:
                    current_streak += 1

        return current_streak

    def get_longest_streak(self):
        entry_dates = self.get_entry_dates()

        longest_streak = 1 if len(entry_dates) else 0

        for entry in entry_dates:
            previous_day = entry - timedelta(days=1)
            if previous_day not in entry_dates:
                next_day = entry + timedelta(days=1)
                streak = 1
                while next_day in entry_dates:
                    next_day += timedelta(days=1)
                    streak += 1
                    longest_streak = max(longest_streak, streak)

        return longest_streak
    
    def get_goal_completed_pct(self):
        if self.units != 'check':
            quantity_list = self.habitentry_set.values_list('quantity', flat=True)
            goals_met = [quantity for quantity in quantity_list if quantity >= self.goal]
            print(len(quantity_list), len(goals_met))

            try:
                goal_completed_pct = round((len(goals_met) / len(quantity_list) * 100), 2)
            except ZeroDivisionError:
                goal_completed_pct = 0

            return goal_completed_pct
        ### might implement checked days / (starting day - today) later. now i cannot set a starting day to test.


class HabitEntry(models.Model):

    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    entry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('habit', 'entry_date')

    def __str__(self):
        return f'{self.habit.name} - {self.entry_date}'