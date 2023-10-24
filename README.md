# Django Habit Tracker

## Steps To Run

Clone the project using the command git clone https://github.com/doyransafa/habit-tracker.git

Create a virtual environment `python -m venv /path/to/new/virtual/environment`

Activate virtual environment `source venv/bin/activate` for MacOS `<venv_path>\Scripts\Activate.ps1` for Windows PowerShell

Install dependencies `pip install -r requirements.txt`

Migrate database `python manage.py migrate`

Start server `python manage.py runserver`

## Features

Login/Logout/Register actions with Django Auth

CRUD functions for habits

Ability to set daily goals for habits (daily repetition, time, distance).

Display current streak, longest streak and goal completion percentage.

Calendar view to mark daily progress

Stats with Chart.js:

Overall:
- Longest Streak by Habits
- Total Records by Habits
- Goal Reach % by Habits

Habit:
- Daily Goal Reach Trend
- Daily Streak Trend

## Stack

- Django
- HTMX
- Chart.js