from tempfile import template
from django.http import HttpResponse
from food.models import Food

from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .models import *
from .forms import *

class listMenu(ListView):
    model = Food
    template_name = 'food/list_menu.html'
class createMenu(CreateView):
    model = Food
    form_class = createForm
    template_name = 'food/create_menu.html'
    succes_url = reverse_lazy('/')

class editMenu(UpdateView):
    model = Food
    form_class = createForm
    template_name = 'food/create_menu.html'
    succes_url = reverse_lazy('/')

# def index(request):
#     salad = 'salad'
#     entrance = 'entrance'
#     desert = 'desert'
#     user = Food(1, salad, entrance, desert)
#     user.save()
#     items = Food.objects.all()
#     return HttpResponse(items.values())

# def post(request):
#     # username = request.POST.get('')
#     salad = 'salad'
#     entrance = 'entrance'
#     desert = 'desert'
#     user = Food(1, salad, entrance, desert)
#     user.save()
#     return HttpResponse("Hello, world. You're at the food index.")