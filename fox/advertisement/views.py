from django.shortcuts import render, redirect

from advertisement.models import Advertisement
from .forms import SearchForm, AddAdvertisementForm



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


def add_advertisement(request):
    return render(request, '../templates/dashboard.html')
