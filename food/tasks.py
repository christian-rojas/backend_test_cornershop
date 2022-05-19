from .models import UserSession
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.contrib.auth.models import User
from django.conf import settings
from backend_test.celery import app

SLACK_TOKEN = getattr(settings, 'SLACK_TOKEN', None)

# slac = "xoxb-3552527527040-3539047250323-PXoe9s14XdR1bc7Q8pRlIZkV"
client = WebClient(SLACK_TOKEN)

@app.task(name="send_message")
def sendSlackMessage(menu, url):
    # la fecha debe coincidir con hoy (para el menu)
    usersRequest = client.api_call("users.list")
    usersIds = []
    if usersRequest['ok']:
        for item in usersRequest['members']:
            if item['is_owner']:
                usersIds.append(item)

    users = User.objects.filter(is_superuser=False).all()

    for user in users:
        u = UserSession()
        u.user = user
        u.menu = menu
        u.save()

        print(user.username)

        user = 'christian.ici17'

        filteredUser = [p for p in usersIds if p['name'] == user]
        # response = client.chat_postMessage(channel='#backend', text="<http://'current_site'> \n :meat_on_bone: \n Choose your meal!")
        response = client.chat_postMessage(channel="@{}".format(filteredUser[0]['id']), blocks=[
            {
            "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Hello! \n I share with you today's menu :meat_on_bone:"
                }
            },
            {
            "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<http://{}/food/menu/{}|Elegir> \n".format(url, u.uuid)
                },
            },
        ])
