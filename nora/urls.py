from django.urls import path
from django.conf.urls import url
from nora import views as core_views
from django.contrib.auth import views as auth_views
# from .views import *


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    path("/login", core_views.login_request, name="login"),
    # url(r'^/create', createMenu.as_view(), name="create")
    # url('/create', createMenu.as_view(), name="create"),
    # url(r'^$', listMenu.as_view(), name="index"),
    # url(r'^/edit/(?P<pk>\d+)$', editMenu.as_view(), name="update")
    url('/signup', core_views.signup, name='signup'),
]