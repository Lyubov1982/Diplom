from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfiProfileForm, NoviceProfileForm, StartupProfileForm
# from .models import CustomUser, UserProfile, ProfiProfile, NoviceProfile, StartupProfile

def register(request):
    role = request.session.get('role')
    if not role:
        messages.error(request, 'Выберите роль перед регистрацией.')
        return redirect('choose_role')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.save()
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form, 'role': role})

def create_profile(request):
    try:
        role = request.user.profile.role
    except UserProfile.DoesNotExist:
        return redirect('create_profile')

    if role == 'professional':
        form_class = ProfiProfileForm
        profile_class = ProfiProfile
    elif role == 'newbie':
        form_class = NoviceProfileForm
        profile_class = NoviceProfile
    elif role == 'startup':
        form_class = StartupProfileForm
        profile_class = StartupProfile
    else:
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()  # Сохраняем ManyToMany поля
            return redirect('profile_detail', user_id=request.user.id)
    else:
        form = form_class()

    return render(request, 'accounts/create_profile.html', {'form': form})

def profile_detail(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('create_profile')

    return render(request, 'accounts/profile_detail.html', {'profile': profile})
