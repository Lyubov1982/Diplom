from django.shortcuts import render


def projects(request):
    return render(request, 'projects/projects.html')


def sport(request):
    return render(request, 'projects/sport.html')


def healthy(request):
    return render(request, 'projects/healthy.html')
