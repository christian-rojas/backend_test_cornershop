# Generated by Django 3.0.8 on 2022-05-12 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='food',
        ),
    ]