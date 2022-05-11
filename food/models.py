from dataclasses import field
from django.db import models
from datetime import date
from django.utils.translation import gettext as _

    # def __str__(self):
    #     return self.task

class Menu(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateField(_("Date"), default=date.today)

class Food(models.Model):
    id = models.AutoField(primary_key = True)
    salad = models.CharField(max_length = 18)
    entrance = models.CharField(max_length = 18)
    desert = models.CharField(max_length = 18)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)