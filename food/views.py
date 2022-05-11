from tempfile import template
from django.http import HttpResponse
from food.models import Food
from django.contrib.auth.models import User
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *

class listMenu(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'food/list_menu.html'
    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):        
    #     return super(listMenu, self).dispatch(request, *args, **kwargs)

class createMenu(LoginRequiredMixin, CreateView):
    model = Food
    form_class = createForm
    template_name = 'food/create_menu.html'
    # succes_url = reverse_lazy('/')

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

# def index(request):
    # salad = 'salad'
    # entrance = 'entrance'
    # desert = 'desert'
    # user = Food(1, salad, entrance, desert)
    # user.save()
    # items = Food.objects.all()
    # User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    # u = User.objects.get(username='john')
    # return HttpResponse(u.is_superuser)

# def post(request):
#     # username = request.POST.get('')
#     salad = 'salad'
#     entrance = 'entrance'
#     desert = 'desert'
#     user = Food(1, salad, entrance, desert)
#     user.save()
#     return HttpResponse("Hello, world. You're at the food index.")