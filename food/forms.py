from dataclasses import fields
from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'
class createForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = ['salad', 'entrance', 'desert']
        # fields = '__all__'

class createMenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['date']
        widgets = {
            'date': DateInput(),
        }

class orderForm(forms.Form):
    class Meta:
        model = Order
        fields = ['food', 'comments']
    # id = forms.IntegerField()
    # comments = forms.CharField(max_length=100, help_text='100 characters max.')