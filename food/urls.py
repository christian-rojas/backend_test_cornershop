from django.urls import path
from django.conf.urls import url
from .views import *

# from . import views

urlpatterns = [
    url(r'^/(?P<id>\d+)$', index, name='index'),

    # url(r'^/(?P<pk>\d+)/food/(?P<id>\d+)$', editFood, name='index'),
    url(r'^/(?P<pk>\d+)/food/edit/(?P<id>\d+)$', editFood, name="update"),

    url(r'^/menu/(?P<uuid>[0-9a-f-]+)', choose, name="choose"),
    # url(r'^/create', createMenu.as_view(), name="create")
    # url('/create', createMenu.as_view(model = Menu, success_url="/food/meals"), name="create"),
    # url('/meals', createFoodMenu.as_view(model = Food, success_url="/meals"), name="food"),
    url('/meals', createMeals),
    url(r'^/create/(?P<id>\d+)$', create_food),
    # url(r'^$', listMenu.as_view(), name="index"),
    url(r'^/edit/(?P<pk>\d+)$', editMenu.as_view(model = Food, success_url="/food"), name="update"),
    url(r'^/delete/(?P<id>\d+)$', delete_view),
    url(r'^/meals/(?P<id>\d+)$', create_food)
]