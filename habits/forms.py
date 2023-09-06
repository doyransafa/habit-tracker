from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):

    class Meta:
        model = Habit
        fields = ['name', 'category', 'units', 'goal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['goal'].widget.attrs['readonly'] = False

    def clean(self):

        cleaned_data = super().clean()
        units = self.cleaned_data.get('units')

        if units == 'check':
            cleaned_data['goal'] = 1
        