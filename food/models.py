from django.db import models
from django.contrib.auth.models import User

class Food(models.Model):
    id = models.AutoField(primary_key = True)
    salad = models.CharField(max_length = 18)
    entrance = models.CharField(max_length = 18)
    desert = models.CharField(max_length = 18)
    # def __str__(self):
    #     return self.task

class Menu(models.Model):
    items = models.ManyToManyField(Food)
