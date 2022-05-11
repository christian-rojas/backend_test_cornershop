from tempfile import template
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

class listMenu(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'food/list_menu.html'
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