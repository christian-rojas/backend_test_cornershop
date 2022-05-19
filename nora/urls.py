from django.conf.urls import url

from nora import views as core_views

# from .views import *


urlpatterns = [
    url("/admin", core_views.admin, name="admin"),
    url("/login", core_views.login_request, name="login"),
    url(r"^/logout$", core_views.log_out, name="logout"),
    url("/signup", core_views.signup, name="signup"),
]
