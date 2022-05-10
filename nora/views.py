# from django.http import HttpResponse
# from django.contrib.auth.models import User
# from .models import *

# # Create your views here.
# def index(request):
#     # user = Food(1, salad, entrance, desert)
#     # user.save()
#     # items = Food.objects.all()
#     User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#     # u = User.objects.get(username='john')
#     # return HttpResponse(u.is_superuser)
#     # user = User()
#     # user.first_name = 'Christian'
#     # user.is_superuser = True
#     # user.password = "pass"
#     # user.email = "christian.ici17@gmail.com"
#     # user.save()
#     # user = User.objects.get(username='john')
#     return HttpResponse(User.objects.all())
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'nora/signup.html', {'form': form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="nora/login.html", context={"login_form":form})

@login_required
def home(request):
    return render(request, 'nora/home.html')
