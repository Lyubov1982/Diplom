import requests
from django.shortcuts import render, redirect
from .models import UsefulLink


def fetch_favicon(url):
    try:
        response = requests.get(f'https://favicongrabber.com/api/grab/{url}')
        response.raise_for_status()
        data = response.json()
        if data['icons']:
            return data['icons'][0]['src']
    except (requests.RequestException, KeyError):
        return None


def add_useful_link(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        title = request.POST.get('title')
        icon_url = fetch_favicon(url)
        UsefulLink.objects.create(title=title, url=url, icon_url=icon_url)
        return redirect('home')
    return render(request, 'projects/add_useful_link.html')


def projects(request):
    useful_links = UsefulLink.objects.all()
    return render(request, 'projects/projects.html', {'useful_links': useful_links})


def sport(request):
    return render(request, 'projects/sport.html')


def healthy(request):
    return render(request, 'projects/healthy.html')
