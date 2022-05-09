from django import forms
from .models import *

class createForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'salad',
            'entrance',
            'desert'
        ]