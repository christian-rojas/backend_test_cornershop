from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse

from slack_sdk import WebClient

from backend_test.celery import app

from .models import Menu, UserSession

SLACK_TOKEN = getattr(settings, "SLACK_TOKEN", None)
client = WebClient(SLACK_TOKEN)


@app.task(name="send_message")
def sendSlackMessage(id, url):
    menu = Menu.objects.get(id=id)

    if menu.date < datetime.now():
        return HttpResponse("menu date expired")

    usersRequest = client.api_call("users.list")
    usersIds = []
    if usersRequest["ok"]:
        for item in usersRequest["members"]:
            if item["is_owner"]:
                usersIds.append(item)

    users = User.objects.filter(is_superuser=False).all()

    for user in users:
        usserSession = UserSession()
        usserSession.user = user
        usserSession.menu = menu
        usserSession.save()

        # user = 'christian.ici17'

        filteredUser = [p for p in usersIds if p["name"] == user]
        client.chat_postMessage(
            channel="@{}".format(filteredUser[0]["id"]),
            text="",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hello! \n I share with you today's menu :meat_on_bone: Have a nice day!",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<http://{}/food/menu/{}|Choose> \n".format(
                            url, usserSession.uuid
                        ),
                    },
                },
            ],
        )
