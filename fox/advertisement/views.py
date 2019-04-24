from django.shortcuts import render, redirect

from advertisement.models import Advertisement
from .forms import SearchForm, AddAdvertisementForm, LoginForm, RegisterForm, ResetPassForm, AddAdvertiserForm


def search(request):
    if request.method == 'GET':
        form = SearchForm()
        ads = Advertisement.objects.all()
        return render(request, '../templates/search.html', {
            'ads': ads,
            'form': form
        })
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            ads = Advertisement.objects.filter(title__contains=title)
            return render(request, '../templates/search.html', {
                'ads': ads,
                'form': form
            })
        else:
            return render(request, '../templates/search.html', {'form': form})


def add_advertisement(request):
    if request.method == 'GET':
        form = AddAdvertisementForm()
        return render(request, '../templates/add_advertisement.html', {'form': form})
    else:
        form = AddAdvertisementForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            form.save()
            return redirect('search')
        else:
            return render(request, '../templates/add_advertisement.html', {'form': form})


def dashboard(request):
    return render(request, '../templates/dashboard.html')


def home(request):
    return render(request, '../templates/home.html')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, '../templates/login.html', {'form': form})
    else:
        form = LoginForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, '../templates/login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        form = AddAdvertiserForm()
        return render(request, '../templates/register.html', {'form': form})
    else:
        form = AddAdvertiserForm(request.POST)
        # form.user = request.user
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request, '../templates/register.html', {'form': form})


def reset_password(request):
    if request.method == 'GET':
        form = ResetPassForm()
        return render(request, '../templates/forget_password.html', {'form': form})
    else:
        form = ResetPassForm(request.POST, request.FILES)
        form.user = request.user
        if form.is_valid():
            form.save()
            return render(request, '../templates/forget_password.html', {'form': form})
        else:
            return render(request, '../templates/forget_password.html', {'form': form})
