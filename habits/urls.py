from django.urls import path
from .views import CreateHabitView, HabitDetailView, HabitListView, UpdateHabitView, DeleteHabitView, date_toggle

urlpatterns = [
    path('', HabitListView.as_view(), name='habit_list'),
    path('habit/create/', CreateHabitView.as_view(), name='create_habit'),
    path('habit/update/<pk>', UpdateHabitView.as_view(), name='update_habit'),
    path('habit/delete/<pk>', DeleteHabitView.as_view(), name='delete_habit'),
    path('habit/details/<pk>', HabitDetailView.as_view(), name='habit_details'),

    path('habit_add_remove/<int:habit_id>/<str:date>', date_toggle, name='date_toggle') 
]