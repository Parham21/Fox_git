from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from advertisement.models import Advertisement, Advertiser, ResetPassword, Category
from advertisement.utils import send_email_async
from .forms import SearchForm, AddAdvertisementForm, LoginForm, ResetPassForm, AddAdvertiserForm, SubmitPassword
from django.contrib.auth import authenticate, login, logout


def search(request):
    query_category = request.GET.get('category')
    if query_category is not None:
        categories = [query_category]
        for category in Category.objects.all():
            if category.parent is not None:
                if category.parent == query_category:
                    categories.append(category.id)
                if category.parent.parent is not None and category.parent.parent == query_category:
                    categories.append(category.id)
    else:
        categories = []
        for category in Category.objects.all():
            if category.parent is not None and category.parent.parent is not None:
                categories.append(category.id)
    if request.method == 'GET':
        form = SearchForm()
        ads = Advertisement.objects.filter(category_id__in=categories)
        return render(request, '../templates/search.html', {
            'categories': categories,
            'ads': ads,
            'form': form
        })
    else:
        form = SearchForm(request.POST)
        if form.is_valid():
            query_params = dict()
            if form.cleaned_data['immediate'] is not None and form.cleaned_data['immediate'] is True:
                query_params['immediate'] = form.cleaned_data['immediate']
            if form.cleaned_data['area'] is not None:
                query_params['area'] = form.cleaned_data['area']
            ads = Advertisement.objects.filter(category_id__in=categories)
            ads = ads.filter(**query_params)
            if form.cleaned_data['title'] is not None:
                ads = ads.filter(title__contains=form.cleaned_data['title'])
            minimum_price = 0
            maximum_price = 100000000000
            if form.cleaned_data['minimum_price'] is not None:
                minimum_price = form.cleaned_data['minimum_price']
            if form.cleaned_data['maximum_price'] is not None:
                minimum_price = form.cleaned_data['maximum_price']
            ads.filter(price__range=(minimum_price, maximum_price))
            if form.cleaned_data['has_image'] is not None and form.cleaned_data['has_image'] is True:
                ads.exclude(image='../static/default.jpg')
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


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, '../templates/login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        user = authenticate(request, username=form['username'].value(), password=form['password'].value())
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, '../templates/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'GET':
        form = AddAdvertiserForm()
        return render(request, '../templates/register.html', {'form': form})
    else:
        form = AddAdvertiserForm(request.POST)
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
        try:
            advertiser = Advertiser.objects.filter(email=form.data['email'])[0]
            new_password = ResetPassword(advertiser=advertiser)
            new_password.save()
            subject = 'Reset Password'
            body = render_to_string('email_template', context={
                'username': advertiser.user.username,
                'reset_link': new_password.get_reset_password_link()
            })
            email = EmailMessage(subject=subject, body=body, to=[advertiser.email])
            send_email_async(email)
            return redirect('home')
        except Advertiser.DoesNotExist:
            return render(request, '../templates/forget_password.html', {
                'form': form,
                'error': 'No user with this email address'
            })


def change_password(request):
    if request.method == 'GET':
        form = SubmitPassword()
        return render(request, '../templates/change_password.html', {'form': form})
    else:
        form = SubmitPassword(request.POST)
        token = request.GET.get('token')
        if form.is_valid():
            new_password = ResetPassword.objects.filter(token=token)[0]
            new_password.advertiser.user.set_password(form.data['password'])
            new_password.advertiser.user.save()
            return redirect('home')
        else:
            return render(request, '../templates/change_password.html', {'form': form})


def advertisement_detail(request, advertisement_id):
    try:
        advertisement = Advertisement.objects.get(pk=advertisement_id)
        related_ads = Advertisement.objects.filter(category=advertisement.category, area=advertisement.area)
        return render(request, '../templates/ad_detail.html', {
            'advertisement': advertisement,
            'related_ads': related_ads,
            'link': request.build_absolute_uri()
        })
    except Advertisement.DoesNotExist:
        raise Http404("Advertisement does not exist")


def favorite_advertisement(request):
    advertiser = Advertiser.objects.filter(user=request.user)
    favorite_ads = advertiser.favorite_ads.all()
    return render(request, '../templates/favorite_ads.html', {
        'favorite_ads': favorite_ads
    })


def add_favorite_advertisement(request, advertisement_id):
    advertiser = Advertiser.objects.filter(user=request.user)
    advertisement = Advertisement.objects.filter(pk=advertisement_id)
    advertiser.favorites_ads.add(advertisement)
    advertiser.save()
    return redirect('advertisement_detail', advertisement_id=advertisement_id)
