from django.conf.urls import url

from .models import Food
from .views import choose, create_food, createMeals, delete_view, editMenu, index

urlpatterns = [
    url(r"^/(?P<id>\d+)$", index, name="index"),
    url(r"^/menu/(?P<uuid>[0-9a-f-]+)", choose, name="choose"),
    url(r"^/menu", createMeals),
    url(r"^/create/(?P<id>\d+)$", create_food),
    url(r"^/edit/(?P<pk>\d+)$", editMenu.as_view(model=Food), name="update"),
    url(r"^/delete/(?P<id>\d+)$", delete_view),
]
