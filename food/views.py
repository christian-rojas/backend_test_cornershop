from tempfile import template
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
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = getattr(settings, 'SLACK_TOKEN', None)

client = WebClient(SLACK_TOKEN)


def index(request, id):
    print(SLACK_TOKEN)
    # pubs = Food.objects.select_related('menu')
    if request.method == 'POST':
        print("ksadkjasjd")
        try:
            response = client.chat_postMessage(channel='#backend', text="Hello world!")
            print(response)
            assert response["message"]["text"] == "Hello world!"
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
            print(f"Got an error: {e.response['error']}")
        return HttpResponseRedirect('/food/' + id)
    # messages.info(request, f"pubs {pubs}.")
    menu =get_object_or_404(Menu, id = id)
    pubs = Food.objects.filter(menu=menu)
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