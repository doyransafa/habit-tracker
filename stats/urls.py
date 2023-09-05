from django.urls import path
from .views import overall_stats, longest_streak_by_habits, total_records_by_habits, goal_reach_pct_by_habits, habit_stats, goal_reach_trend, streak_trend


urlpatterns = [
    path('', overall_stats, name='overall_stats'),
    path('longest', longest_streak_by_habits, name='longest_streak_by_habits'),
    path('total_records', total_records_by_habits, name='total_records'),
    path('goals_reached', goal_reach_pct_by_habits, name='goals_reached'),

    path('<int:pk>/<int:month>', habit_stats, name='habit_stats'),

    path('goal_reach_trend/<int:pk>/<int:month>',goal_reach_trend, name='goal_reach_trend'),
    path('streak_trend/<int:pk>/<int:month>',streak_trend, name='streak_trend'),
]
