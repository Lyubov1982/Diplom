from django.db.models import Q
from .models import Project, Tag
from users.models import Profile, Photo, Video
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def search_projects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    pr = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    return pr, search_query


def search_news_feed(request):
    search_query = request.GET.get('search_query', '')
    if search_query:
        profiles = Profile.objects.distinct().filter(name__icontains=search_query).order_by('name')  # Добавляем сортировку
        photos = Photo.objects.distinct().filter(caption__icontains=search_query).order_by('-created')
        videos = Video.objects.distinct().filter(caption__icontains=search_query).order_by('-created')
    else:
        profiles = Profile.objects.all().order_by('name')  # Добавляем сортировку
        photos = Photo.objects.all().order_by('-created')
        videos = Video.objects.all().order_by('-created')

    return profiles, photos, videos, search_query


def paginate_projects(request, pr, results):
    page = request.GET.get('page')
    # results = 6
    paginator = Paginator(pr, results)

    try:
        pr = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        pr = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        pr = paginator.page(page)

    right_index = int(page) + 4

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1

    custom_range = range(left_index, right_index)
    return custom_range, pr


def paginate_news(request, pr, results):
    page = request.GET.get('page')
    paginator = Paginator(pr, results)

    try:
        pr = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        pr = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        pr = paginator.page(page)

    right_index = int(page) + 4

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    left_index = int(page) - 4

    if left_index < 1:
        left_index = 1

    custom_range = range(left_index, right_index)
    return custom_range, pr
