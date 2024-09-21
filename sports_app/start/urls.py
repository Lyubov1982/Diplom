# start/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Маршрут для главной страницы
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path('choose_role/', views.choose_role, name='choose_role'),
]
