from django.shortcuts import render

from django_slack import slack_message

# Create your views here.
def send():
    return slack_message('/slack/message.html', "Hola Mundo")

