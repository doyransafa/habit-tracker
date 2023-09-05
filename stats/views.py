from django.shortcuts import render
from django.http import JsonResponse
from habits.models import Habit, HabitEntry
from datetime import date, timedelta

# Create your views here.

colors = ['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099', '#3B3EAC', '#0099C6', '#DD4477', '#66AA00', '#B82E2E',
          '#316395', '#994499', '#22AA99', '#AAAA11', '#6633CC', '#E67300', '#8B0707', '#329262', '#5574A6', '#3B3EAC']
months = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


def overall_stats(request):

    habits = Habit.objects.all().filter(user=request.user.id)
    streaks = [habit.get_longest_streak() for habit in habits]
    longest_streak = max(streaks)
    goal_reach_total = 0

    for habit in habits:
        entries = habit.habitentry_set.values_list('quantity', flat=True)
        goals_met = [entry for entry in entries if entry >= habit.goal]
        goal_reach_total += len(goals_met)

    month = date.today().month

    context = {
        'habits': habits,
        'longest_streak': longest_streak,
        'goal_reach_total': goal_reach_total,
        'month': month,

    }

    return render(request, 'overall_stats.html', context)


def longest_streak_by_habits(request):

    habits = Habit.objects.all().filter(user=request.user.id)

    labels = [habit.name for habit in habits]
    values = [habit.get_longest_streak() for habit in habits]
    datasets = []

    for i, habit in enumerate(habits):
        dataset = {
            'label': labels[i],
            'backgroundColor': colors[i],
            'borderColor': colors[i],
            'data': [values[i]]
        }
        datasets.append(dataset)

    data = {'labels': ['Longest Streak by Habits'],
            'datasets': datasets}

    return JsonResponse({
        'type': "bar",
        'data': data,
        'options': {
            'title': {
                'text': "Longest Streak by Habits",
                'display': 'true'
            }
        }
    })


def total_records_by_habits(request):

    habits = Habit.objects.all().filter(user=request.user.id)

    labels = [habit.name for habit in habits]
    values = [len(habit.habitentry_set.all()) for habit in habits]

    datasets = []

    for i, habit in enumerate(habits):
        dataset = {
            'label': labels[i],
            'backgroundColor': colors[i],
            'borderColor': colors[i],
            'data': [values[i]]
        }
        datasets.append(dataset)

    data = {'labels': ['Total Records by Habits'],
            'datasets': datasets}

    return JsonResponse({
        'type': "bar",
        'data': data,
        'options': {
            'title': {
                'text': "Total Records by Habits",
                'display': 'true'
            }
        }
    })


def goal_reach_pct_by_habits(request):

    habits = Habit.objects.all().filter(user=request.user.id)

    labels = [habit.name for habit in habits]
    values = [habit.get_goal_completed_pct() for habit in habits]

    datasets = []

    for i, _ in enumerate(habits):
        dataset = {
            'label': labels[i],
            'backgroundColor': colors[i],
            'borderColor': colors[i],
            'data': [values[i]]
        }
        datasets.append(dataset)

    data = {'labels': ['Goal Reach Pct. by Habit'],
            'datasets': datasets}

    return JsonResponse({
        'type': "bar",
        'data': data,
        'options': {
            'title': {
                'text': "Goal Reach Pct. by Habit",
                'display': 'true'
            },
            'scales': {
                'y': {
                    'max': 100,
                    'min': 0,
                }
            }
        },

    })


def habit_stats(request, pk, month):

    habit = Habit.objects.get(pk=pk)
    user_habits = Habit.objects.all().filter(user=request.user)

    context = {
        'habit': habit,
        'user_habits': user_habits,
        'month' : {
            'str' : months[month-1],
            'int' : month,
            'previous' : month - 1 if month > 1 else month,
            'next': month + 1 if month < 12 else month,
        }
    }

    return render(request, 'habit_stats.html', context)


def goal_reach_trend(request,pk, month):

    habit = Habit.objects.get(pk=pk)
    habit_goal = habit.goal

    entry_dates = list(habit.get_entry_dates())

    year_list = habit.get_year_list()

    month_days = year_list[month - 1]

    quantity_list = habit.habitentry_set.values_list('quantity', flat=True)

    values = []
    for day in month_days:
        if day in entry_dates:
            day_index = entry_dates.index(day)
            values.append(quantity_list[day_index])
        else:
            values.append(0)

    chart_json = {
        'type': 'line',
        'data': {
            'labels': list(month_days),
            'datasets': [
                {
                    'label': 'Records',
                    'fill': 'false',
                    'backgroundColor': colors[3],
                    'borderColor': colors[3],
                    'data': values,
                }, {
                    'label': 'Goal',
                    'fill': 'false',
                    'backgroundColor': colors[2],
                    'borderColor': colors[2],
                    'borderDash': [5, 5],
                    'data': [habit_goal for goal in values],
                }
            ]
        },
        'options': {
            'responsive': 'true',
            'plugins': {
                'title': {
                    'display': 'true',
                    'text': 'Chart.js Line Chart'
                },
            },
            'interaction': {
                'mode': 'index',
                'intersect': 'false'
            },
            'scales': {
                'x': {
                    'display': 'true',
                    'title': {
                        'display': 'true',
                        'text': 'Month'
                    }
                },
                'y': {
                    'display': 'true',
                    'title': {
                        'display': 'true',
                        'text': 'Value'
                    }
                }
            }
        },
    }

    return JsonResponse(chart_json)
    

def streak_trend(request, pk, month):

    habit = Habit.objects.get(pk=pk)

    year_list = habit.get_year_list()
    
    month_days = year_list[month - 1]

    entry_dates = list(habit.get_entry_dates().order_by('entry_date'))

    entry_tuples = []

    current_streak = 1
    for i, entry in enumerate(entry_dates):
        previous_day = entry - timedelta(days=1)
        if previous_day not in entry_dates:
            current_streak = 1
        else:
            current_streak += 1
        entry_tuples.append((entry, current_streak))

    monthly_entry_tuples = [entry for entry in entry_tuples if entry[0] in month_days]

    if len(monthly_entry_tuples) > 0:
        monthly_entries, monthly_entry_values = zip(*monthly_entry_tuples)
    else: 
        monthly_entries, monthly_entry_values = [],[]

    values = []
    for day in month_days:
        if day in monthly_entries:
            index = monthly_entries.index(day)
            values.append(monthly_entry_values[index])
        else:
            values.append(0)

    chart_json = {
        'type': 'line',
        'data': {
            'labels': list(month_days),
            'datasets': [
                {
                    'label': 'Records',
                    'fill': 'false',
                    'backgroundColor': colors[4],
                    'borderColor': colors[4],
                    'data': values,
                }
            ]
        },
        'options': {
            'responsive': 'true',
            'plugins': {
                'title': {
                    'display': 'true',
                    'text': 'Chart.js Line Chart'
                },
            },
            'interaction': {
                'mode': 'index',
                'intersect': 'false'
            },
            'scales': {
                'x': {
                    'display': 'true',
                    'title': {
                        'display': 'true',
                        'text': 'Month'
                    }
                },
                'y': {
                    'display': 'true',
                    'title': {
                        'display': 'true',
                        'text': 'Value'
                    },
                    'min': 0,
                    'step' : 1,
                }
            }
        },
    }

    print(entry_dates)
    print(entry_tuples)
    print(monthly_entry_tuples)
    print(monthly_entries)
    print(monthly_entry_values)
    print(values)

    return JsonResponse(chart_json)
