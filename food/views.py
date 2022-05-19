from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from forms import createForm, createMenuForm, orderForm
from models import Food, Menu, Order, UserSession
from slack_sdk.errors import SlackApiError
from tasks import sendSlackMessage


@login_required
def index(request, id):
    current_site = get_current_site(request)
    # order = Order.objects.get(id=1)
    if request.method == "POST":
        try:
            sendSlackMessage.delay(id, str(current_site))
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
        return HttpResponseRedirect("/food/" + id)

    menu = get_object_or_404(Menu, id=id)

    foodLists = Food.objects.filter(menu=menu)
    if not foodLists.exists():
        return HttpResponse("the menu does not contain any meal")
    form = foodLists
    return render(
        request,
        "food/food_list.html",
        {"forms": form, "date": form[0].menu.date, "id": form[0].menu.id},
    )


class createFoodMenu(LoginRequiredMixin, CreateView):
    model = Food
    form_class = createForm
    template_name = "food/create_food.html"
    # succes_url = reverse_lazy('/')


class createMenu(LoginRequiredMixin, CreateView):
    model = Menu
    form_class = createMenuForm
    template_name = "food/create_menu.html"


class editMenu(LoginRequiredMixin, UpdateView):
    model = Food
    form_class = createForm
    template_name = "food/create_menu.html"

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("index", kwargs={"id": pk})


def delete_view(request, id):
    context = {}
    obj = get_object_or_404(Food, id=id)
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/food")
    return render(request, "food/delete_menu.html", context)


def create_food(request, id):
    if request.method == "POST":
        form = createForm(request.POST)
        print(request.POST)
        if form.is_valid():
            menu = get_object_or_404(Menu, id=id)
            food = Food()
            food.salad = form.cleaned_data["salad"]
            food.entrance = form.cleaned_data["entrance"]
            food.desert = form.cleaned_data["desert"]
            food.menu = menu
            food.save()
            menu.food = food
            menu.save()

            return HttpResponseRedirect("/food")
    else:
        form = createForm()
    return render(request, "food/create.html", {form: form})


def createMeals(request):
    if request.method == "POST":
        form = createMenuForm(request.POST)
        if form.is_valid():
            menu = Menu()
            menu.date = form.cleaned_data["date"]
            menu.save()
            return HttpResponseRedirect("/food")
    else:
        form = createMenuForm()

    return render(request, "food/create_meal.html", {form: form})


def choose(request, uuid):

    session = UserSession.objects.get(uuid=uuid)
    try:
        Order.objects.get(session=session)
        return render(request, "menu/error.html")
    except Order.DoesNotExist:
        print("no existe")

    pubs = Food.objects.filter(menu=session.menu)
    form = orderForm(request.POST)

    currentTime = datetime.now()
    currentHour = currentTime.hour

    if currentHour >= 22:
        return render(request, "menu/late.html")

    if request.method == "POST" and form.is_valid():
        if currentHour >= 22:
            return render(request, "menu/late.html")
        food = get_object_or_404(Food, id=request.POST["id"])
        order = Order()
        order.food = food
        order.session = session
        order.comments = request.POST["comments"]
        order.save()
        return HttpResponseRedirect("/home")

    form = pubs
    return render(request, "menu/choose.html", {"forms": form})
