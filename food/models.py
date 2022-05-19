import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _

# def __str__(self):
#     return self.task


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(_("Date"), default=date.today)


class Food(models.Model):
    id = models.AutoField(primary_key=True)
    salad = models.CharField(max_length=18)
    entrance = models.CharField(max_length=18)
    desert = models.CharField(max_length=18)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu")


class UserSession(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="user_menu")


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="order_food")
    session = models.ForeignKey(
        UserSession, on_delete=models.CASCADE, related_name="order_session"
    )
    comments = models.CharField(max_length=28)
    # other fields here
    # customizations = models.CharField(max_length = 256)

    # def get_absolute_url(self):
    #     return reverse('lawyer_detail', kwargs={'lawyer_slug': self.lawyer_slug})
