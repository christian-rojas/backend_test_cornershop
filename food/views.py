from tempfile import template
from time import clock_getres
from urllib import request
from django.http import HttpResponse
from food.models import Food
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .models import *
from .forms import *
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.conf import settings
# from slack.views import send
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.contrib.sites.shortcuts import get_current_site
from .tasks import sendSlackMessage

SLACK_TOKEN = getattr(settings, 'SLACK_TOKEN', None)

# slac = "xoxb-3552527527040-3539047250323-PXoe9s14XdR1bc7Q8pRlIZkV"
client = WebClient(SLACK_TOKEN)


def index(request, id):
    current_site = get_current_site(request)
    menu = get_object_or_404(Menu, id=id)

    order = Order.objects.get(id=1)
    print(order.comments)

    # menus = Menu.objects.all()
    # print("fecha: " + str(len(menus)))
    # user = UserSession.objects.all()
    # print(user)
    # user = User.objects.get(id=2)
    # userSession = UserSession.objects.get(user=user)
    # requesto = client.api_call("users.list")
    # if requesto['ok']:
    #     for item in requesto['members']:
    #         if item['is_owner']:
    #             user_id = item['id']

    # user_channel = client.conversations_open(users=user_id, return_im=True)
    # print(user_channel)
    
    # print(current_site.name)
    # pubs = Food.objects.select_related('menu')
    if request.method == 'POST':
        try:
            sendSlackMessage(menu, current_site)
            # u = UserSession()
            # u.user = user
            # u.menu = menu
            # u.save()
            # response = client.chat_postMessage(channel='#backend', text="<http://'current_site'> \n :meat_on_bone: \n Choose your meal!")
            # response = client.chat_postMessage(channel="@{}".format(user_id), blocks=[
            #     {
            #     "type": "section",
            #         "text": {
            #             "type": "mrkdwn",
            #             "text": "Hello! \n I share with you today's menu :meat_on_bone:"
            #         }
            #     },
            #     {
            #     "type": "section",
            #         "text": {
            #             "type": "mrkdwn",
            #             "text": "<http://{}/food/menu/{}|Elegir> \n".format(current_site, u.uuid)
            #         },
            #     },
            # ])
            

            # isCreated = Order.objects.create(menu=menu, session=user)
            # print(isCreated)


            # response = client.conversations_open(users=user_id)
            # client.chat_postMessage(channel=response['channel']['id'], text="hola")
            # token="xoxb-3552527527040-3526276886085-WCEpVcsG8ZlDBjFzG0Ip6j2F",
            # print(user_id)
            # response = client.conversations_open(users=user_id)
            # response = client.chat_postMessage(channel="@{}".format(user_id), text="noooo")

            
            # print(response)
            # assert response["message"]["text"] == "Hello world!"
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
        return HttpResponseRedirect('/food/' + id)
    # messages.info(request, f"pubs {pubs}.")
    
    pubs = Food.objects.filter(menu=menu)
    # print(menu.uuid)
    form = (pubs)
    return render(request, 'food/list_menu.html', {"forms":form, "date": form[0].menu.date, "id": form[0].menu.id})
# class listMenu(LoginRequiredMixin, ListView):
#     model = Menu
#     template_name = 'food/list_menu.html'
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):        
    #     return super(listMenu, self).dispatch(request, *args, **kwargs)

class createFoodMenu(LoginRequiredMixin, CreateView):
    model = Food
    form_class = createForm
    template_name = 'food/create_food.html'
    # succes_url = reverse_lazy('/')

class createMenu(LoginRequiredMixin, CreateView):
    model = Menu
    form_class = createMenuForm
    template_name = 'food/create_menu.html'

class editMenu(LoginRequiredMixin, UpdateView):
    model = Food
    form_class = createForm
    template_name = 'food/create_menu.html'

def editFood(request, id, pk):
    if request.method == 'POST':
        form = createForm(request.POST)
        print(request.POST)
        if form.is_valid():
            food = get_object_or_404(Food, id = id)
            food.salad = form.cleaned_data['salad']
            food.entrance = form.cleaned_data['entrance']
            food.desert = form.cleaned_data['desert']
            food.save()
            #TODO: pasarle el id a la url
            return HttpResponseRedirect('/food/' + pk)
    else:
        form = get_object_or_404(Food, id = id)
        # food = get_object_or_404(Food, id = id)
        # print(food.salad)
        # form = food

    return render(request, 'food/create_foo.html', {'form': form})

    # succes_url = reverse_lazy('/')
def delete_view(request, id):
    context ={}
    print(id)
    obj = get_object_or_404(Food, id = id)
    if request.method =="POST":
        obj.delete()
        return HttpResponseRedirect("/food")
 
    return render(request, "food/delete_menu.html", context)

def create_food(request, id):
    if request.method == 'POST':
        form = createForm(request.POST)
        print(request.POST)
        if form.is_valid():
            menu = get_object_or_404(Menu, id = id)
           
            food = Food()
            food.salad = form.cleaned_data['salad']
            food.entrance = form.cleaned_data['entrance']
            food.desert = form.cleaned_data['desert']
            food.menu = menu
            food.save()

            menu.food = food
            menu.save()

            return HttpResponseRedirect('/food')
    else:
        form = createForm()
    return render(request, 'food/create_foo.html', {form: form})

def createMeals(request):
    if request.method == 'POST':
        form = createMenuForm(request.POST)
        if form.is_valid():
            menu = Menu()
            menu.date = form.cleaned_data['date']
            menu.save()
            #TODO: pasarle el id a la url
            return HttpResponseRedirect('/food')
    else:
        form = createMenuForm()

    return render(request, 'food/create_meal.html', {form: form})

def choose(request, uuid):
    # userSession = get_object_or_404(UserSession, uuid = uuid)
    session = UserSession.objects.get(uuid=uuid)
    pubs = Food.objects.filter(menu=session.menu)
    form = orderForm(request.POST)

    now = datetime.now().hour
    # current_time = now.strftime("%H:%M:%S")
    print("Current Time =", now)

    if now >= 8:
        return render(request, 'menu/late.html')

    if request.method == 'POST' and form.is_valid():
        now = datetime.now().hour
        if now >= 8:
            return render(request, 'menu/late.html')
        food = get_object_or_404(Food, id = request.POST["id"])
        order = Order()
        order.food = food
        order.session = session
        order.comments = form.cleaned_data['comments']
        order.save()
        #TODO: logica de insercion en orders
        return HttpResponseRedirect('/food')

    # print(menu.uuid)
    form = (pubs)
    return render(request, 'menu/choose.html', {"forms": form})

# necesito mandar un uuid, podria ser un modelo con el user_id, el menu_id y el uuid, comments, food_id
# y cuando el user responda lleno lo demas