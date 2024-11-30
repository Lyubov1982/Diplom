import requests
from django.shortcuts import render, redirect
from .models import UsefulLink, Project, Section, Tag, Comment
from users.models import Profile, Photo, Video
from .forms import ProjectForm, TagForm, UsefulLinkForm, CommentForm
from users.forms import PhotoForm, VideoForm
from django.contrib.auth.decorators import login_required
from .utils import search_projects, search_news_feed, paginate_projects, paginate_news
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ckeditor_uploader.widgets import CKEditorUploadingWidget






def fetch_favicon(url):
    try:
        response = requests.get(f'https://favicongrabber.com/api/grab/{url}')
        response.raise_for_status()
        data = response.json()
        if data['icons']:
            return data['icons'][0]['src']
    except (requests.RequestException, KeyError):
        return None


def projects(request):
    useful_links = UsefulLink.objects.all()
    sections = Section.objects.all()
    pr, search_query = search_projects(request)

    # Фильтрация по категориям и тегам
    selected_section = request.GET.get('section')
    selected_tag = request.GET.get('tag')

    if selected_section:
        pr = pr.filter(sections__name=selected_section)

    if selected_tag:
        pr = pr.filter(tags__name=selected_tag)

    custom_range, pr = paginate_projects(request, pr, 6)

    unique_tags = Tag.objects.all()

    context = {
        'unique_tags': unique_tags,
        'useful_links': useful_links,
        'sections': sections,
        'search_query': search_query,
        'custom_range': custom_range,
        'projects': pr,
        'background_image': 'images/one.jpg',
        'selected_section': selected_section,
        'selected_tag': selected_tag,
    }
    return render(request, 'projects/projects.html', context)


@login_required(login_url='login')
def project(request, pk):
    project_obj = Project.objects.get(id=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.profile = request.user.profile if hasattr(request.user, 'profile') else None
            comment.project = project_obj
            comment.save()
            return redirect('project', pk=pk)
    else:
        form = CommentForm()

    context = {
        'background_image': 'images/one.jpg',
        'hide_search': True,  # Добавляем переменную для скрытия поисковой строки
        'project': project_obj,
        'form': form,
    }
    return render(request, 'projects/single-project.html', context)


# def create_project(request):
#     profile = request.user.profile
#     project_form = ProjectForm()
#     tag_form = TagForm()
#
#     if request.method == "POST":
#         project_form = ProjectForm(request.POST, request.FILES)
#         tag_form = TagForm(request.POST)
#         if project_form.is_valid():
#             project = project_form.save(commit=False)
#             project.owner = profile
#             project.save()
#             return redirect('account')
#
#         if 'add_tag' in request.POST:
#             if tag_form.is_valid():
#                 tag_form.save()
#                 return redirect('create-project')
#
#         if 'submit_project' in request.POST:
#             if project_form.is_valid():
#                 project = project_form.save()
#                 return redirect('account')
#
#     context = {
#         'background_image': 'images/free1.jpg',
#         'hide_search': True,  # Добавляем переменную для скрытия поисковой строки
#         'project_form': project_form,
#         'tag_form': tag_form,
#     }
#     return render(request, 'projects/form-template.html', context)



def create_project(request):
    profile = request.user.profile
    project_form = ProjectForm()
    tag_form = TagForm()

    if request.method == "POST":
        project_form = ProjectForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)

        if 'add_tag' in request.POST:
            if tag_form.is_valid():
                tag_form.save()
                return redirect('create-project')

        if 'submit_project' in request.POST:
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.owner = profile
                project.save()

                # Добавляем выбранные теги и секции
                project.tags.set(project_form.cleaned_data['tags'])
                project.sections.set(project_form.cleaned_data['sections'])

                return redirect('account')

    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,  # Добавляем переменную для скрытия поисковой строки
        'project_form': project_form,
        'tag_form': tag_form,
    }
    return render(request, 'projects/form-template.html', context)


def news_feed(request):
    profiles, photos, videos, search_query = search_news_feed(request)

    # Объединяем фотографии и видео в один список и сортируем по дате создания
    news_feed_items = sorted(
        list(photos) + list(videos),
        key=lambda x: x.created,
        reverse=True
    )

    custom_range, news_feed_items = paginate_news(request, news_feed_items, 6)

    # Получаем все комментарии для всех проектов
    all_comments = Comment.objects.all().order_by('-created_at')

    context = {
        'background_image': 'images/two.jpg',
        'search_query': search_query,
        'profiles': profiles,
        'news_feed_items': news_feed_items,
        'all_comments': all_comments,
        'custom_range': custom_range
    }
    return render(request, 'projects/news_feed.html', context)


def shop(request):
    context = {
        'hide_search': True,
        'background_image': 'images/shop.jpg',
    }
    return render(request, 'projects/shop.html', context)


@login_required(login_url='login')
def add_useful_link(request):
    if request.method == 'POST':
        form = UsefulLinkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    else:
        form = UsefulLinkForm()

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'form': form
    }
    return render(request, 'projects/add_useful_link.html', context)


@login_required(login_url='login')
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.profile = request.user.profile
            photo.save()
            return redirect('news_feed')
    else:
        form = PhotoForm()
    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'form': form
    }
    return render(request, 'projects/upload_photo.html', context)


@login_required(login_url='login')
def update_photo(request, pk):
    profile = request.user.profile
    try:
        photo = profile.photos.get(id=pk)
    except Photo.DoesNotExist:
        return redirect('news_feed')  # или другой обработчик ошибок

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = PhotoForm(instance=photo)

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'photo': photo,
        'form': form
    }
    return render(request, 'projects/upload_photo.html', context)


@login_required(login_url='login')
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.profile = request.user.profile
            video.save()
            return redirect('news_feed')
    else:
        form = VideoForm()

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'form': form
    }
    return render(request, 'projects/upload_video.html', context)


@login_required(login_url='login')
def update_video(request, pk):
    profile = request.user.profile
    video = profile.videos.get(id=pk)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('news_feed')
    else:
        form = VideoForm(instance=video)

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'video': video,
        'form': form
    }
    return render(request, 'projects/upload_video.html', context)


@login_required(login_url='login')
def add_content(request):
    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,  # Добавляем переменную для скрытия поисковой строки
    }
    return render(request, 'projects/add_content.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        return redirect('news_feed')  # или другой обработчик ошибок

    project_form = ProjectForm(instance=project)
    tag_form = TagForm()

    if request.method == "POST":
        project_form = ProjectForm(request.POST, request.FILES, instance=project)
        if project_form.is_valid():
            project_form.save()
            return redirect('account')

        tag_form = TagForm(request.POST)
        if 'add_tag' in request.POST:
            if tag_form.is_valid():
                tag = tag_form.save()
                project.tags.add(tag)
                return redirect('account')

        if 'submit_project' in request.POST:
            if project_form.is_valid():
                project_form.save()
                return redirect('account')

    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,  # Добавляем переменную для скрытия поисковой строки
        'project_form': project_form,
        'tag_form': tag_form,
        'project': project,
    }
    return render(request, 'projects/form-template.html', context)


def delete_project(request, pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        return redirect('news_feed')

    if request.method == "POST":
        project.delete()
        return redirect('account')

    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,
        'object': project,
    }
    return render(request, 'projects/delete_template.html', context)


def delete_video(request, pk):
    profile = request.user.profile
    try:
        video = profile.videos.get(id=pk)
    except Video.DoesNotExist:
        return redirect('news_feed')

    if request.method == "POST":
        video.delete()
        return redirect('account')

    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,
        'object': video,
    }
    return render(request, 'projects/delete_template.html', context)


def delete_photo(request, pk):
    profile = request.user.profile
    try:
        photo = profile.photos.get(id=pk)
    except Photo.DoesNotExist:
        return redirect('news_feed')

    if request.method == "POST":
        photo.delete()
        return redirect('account')

    context = {
        'background_image': 'images/free1.jpg',
        'hide_search': True,
        'object': photo,
    }
    return render(request, 'projects/delete_template.html', context)


def like_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user in project.likes.all():
        project.likes.remove(request.user)
    else:
        project.likes.add(request.user)
    project.save()
    return JsonResponse({'likes_count': project.likes.count()})


@csrf_exempt
def get_comments(request, pk):
    if request.method == 'GET':
        project_obj = get_object_or_404(Project, id=pk)
        comments = Comment.objects.filter(project=project_obj).order_by('-created_at')
        comments_list = [{
            'author': comment.author.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
        return JsonResponse({'comments': comments_list})
