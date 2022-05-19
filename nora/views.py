from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render

from slack_sdk.errors import SlackApiError

from food.models import Menu
from food.tasks import sendSlackMessage


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, template_name="nora/base.html")
    else:
        form = UserCreationForm()
    return render(request, "nora/signup.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            print(user.is_authenticated)
            if user.is_superuser:
                return admin(request)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return render(request, template_name="food/base.html")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="nora/login.html", context={"login_form": form}
    )


def home(request):
    return render(request, "nora/base.html")


@login_required
def admin(request):
    menus = Menu.objects.all()
    menus = menus.exists() and menus.values()

    current_site = get_current_site(request)
    if request.method == "POST":
        id = request.POST["menu_id"]
        try:
            sendSlackMessage.delay(id, str(current_site))
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        return HttpResponseRedirect("/nora/admin")

    return render(request, "food/list_menu.html", {"forms": menus})


@login_required
def log_out(request):
    logout(request)
    return render(request, template_name="nora/login.html")
