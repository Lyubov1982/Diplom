from django.shortcuts import render, redirect
from .models import Profile, Photo, Video
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, paginate_profiles
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



def profiles(request):
    prof, search_query = search_profiles(request)
    custom_range, prof = paginate_profiles(request, prof, 6)
    context = {
        # 'hide_search': True,
        'background_image': 'images/sport.jpg',
        'profiles': prof,
        'search_query': search_query
    }
    return render(request, 'users/index.html', context)


@login_required(login_url='login')
def user_profile(request, pk):
    prof = get_object_or_404(Profile, id=pk)

    top_skills = prof.skill_set.exclude(info__exact="")
    other_skills = prof.skill_set.filter(info="")

    # Фильтрация по тегам
    selected_tag = request.GET.get('tag')
    if selected_tag:
        projects = prof.project_set.filter(tags__name=selected_tag)
    else:
        projects = prof.project_set.all()

    context = {
        'hide_search': True,
        'background_image': 'images/free.jpg',
        'profile': prof,
        'top_skills': top_skills,
        'other_skills': other_skills,
        'projects': projects,
        'selected_tag': selected_tag,
    }
    return render(request, 'users/profile.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.error(request, "Имя пользователя не существует")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('projects')  # перенаправление пользователя при авторизации
        else:
            messages.error(request, "Неверное имя пользователя или пароль")
    context = {
        'hide_search': True,
        'background_image': 'images/sport2.jpg',
    }
    return render(request, 'users/login_register.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, "Вы вышли из системы!")
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Учетная запись пользователя была создана!")
            login(request, user)
            return redirect('offer_profile_creation')  # Перенаправление на предложение создания профиля
        else:
            messages.error(request, "Во время регистрации произошла ошибка.")

    context = {
        'page': page,
        'hide_search': True,
        'background_image': 'images/sport2.jpg',
        'form': form
    }
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login')
def create_profile(request):
    try:
        # Попытка получить существующий профиль пользователя
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Если профиля не существует, создаем новый
        profile = None

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.name = f"{request.user.first_name} {request.user.last_name}"
            profile.email = request.user.email  # Устанавливаем email пользователя
            profile.save()
            return redirect('user_profile', pk=profile.id)
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'hide_search': True,
        'background_image': 'images/account.jpg',
        'profile_form': profile_form,
    }
    return render(request, 'users/create_profile.html', context)


@login_required(login_url='login')
def offer_profile_creation(request):
    if request.method == 'POST':
        if 'create_profile' in request.POST:
            return redirect('create_profile')
        elif 'skip_profile' in request.POST:
            return redirect('projects')
    context = {
        'hide_search': True,
        'background_image': 'images/create.jpg',
    }
    return render(request, 'users/offer_profile_creation.html', context)


@login_required(login_url='login')
def user_account(request):
    prof = request.user.profile
    skills = prof.skill_set.all()
    context = {
        'hide_search': True,
        'background_image': 'images/account.jpg',
        'profile': prof,
        'skills': skills,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'hide_search': True,
        'background_image': 'images/account.jpg',
        'form': form,
    }
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.expert = profile
            skill.save()

            messages.success(request, 'Skill успешно добавлен!')
            return redirect('account')

    context = {
        'hide_search': True,
        'background_image': 'images/sport2.jpg',
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill обновлен!')
            return redirect('account')

    context = {
        'hide_search': True,
        'background_image': 'images/sport2.jpg',
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, 'Skill удален!')
        return redirect('account')

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'object': skill
    }
    return render(request, 'users/delete-skill.html', context)


def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return JsonResponse({'likes_count': photo.likes.count()})


def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)
    return JsonResponse({'likes_count': video.likes.count()})


@login_required(login_url='login')
def created_message(request, pk):
    recipient = get_object_or_404(Profile, id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient

            if request.user.is_authenticated:
                message.name = request.user.profile.name
                message.email = request.user.profile.email

            message.save()

            messages.success(request, 'Ваше сообщение успешно отправлено!')
            return redirect('user_profile', pk=recipient.id)

    context = {
        'hide_search': True,
        'background_image': 'images/free1.jpg',
        'recipient': recipient,
        'form': form
               }
    return render(request, 'users/message_form.html', context)


