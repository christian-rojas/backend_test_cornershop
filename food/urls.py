from django.urls import path
# from django.conf.urls import url
# from .views import *

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # url(r'^create/', createMenu.as_view(), name="create")
]