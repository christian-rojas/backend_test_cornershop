from django.urls import path
from django.conf.urls import url
from .views import *

# from . import views

urlpatterns = [
    # path('/index', views.index, name='index'),
    # url(r'^/create', createMenu.as_view(), name="create")
    url('/create', createMenu.as_view(model = Food, success_url="/food"), name="create"),
    url(r'^$', listMenu.as_view(), name="index"),
    url(r'^/edit/(?P<pk>\d+)$', editMenu.as_view(model = Food, success_url="/food"), name="update"),
    url(r'^/delete/(?P<id>\d+)$', delete_view),
]