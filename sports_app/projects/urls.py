from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('sport/', views.sport, name='sport'),
    path('healthy/', views.healthy, name='healthy'),
    path('add-useful-link/', views.add_useful_link, name='add-useful-link'),
]
