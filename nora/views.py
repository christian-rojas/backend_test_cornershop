from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from food.models import UserSession
import json

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return render(request, template_name="nora/base.html")
	else:
		form=UserCreationForm()
	return render(request, 'nora/signup.html', {'form': form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			# userSession = UserSession.objects.select_related().get(user=user)
			# print(userSession.user.id)
			if user.is_superuser:
				print("is superuser") 
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return render(request, template_name="food/list_menu.html")
				# return redirect('admin')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="nora/login.html", context={"login_form":form})

@login_required
def home(request):
    return render(request, 'nora/base.html')

@login_required
def admin(request):
    return render(request, 'food/list_menu.html')

@login_required
def log_out(request):
    logout(request)
    return render(request, template_name="nora/login.html")

