# start/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate


def index(request):
    return render(request, 'start/index.html')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('choose_role')  # Перенаправление на домашнюю страницу после регистрации
    else:
        form = UserCreationForm()
    return render(request, 'start/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправление на домашнюю страницу после входа
    else:
        form = AuthenticationForm()
    return render(request, 'start/login.html', {'form': form})


def home(request):
    return render(request, 'start/home.html')

def choose_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        request.session['role'] = role
        return redirect('register') # account
    return render(request, 'account/choose_role.html') # ???
