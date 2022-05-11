from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
class createForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['salad', 'entrance', 'desert']

class createMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['date']
        widgets = {
            'date': DateInput(),
        }