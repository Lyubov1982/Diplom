from django.urls import path
from . import views

urlpatterns = [
    path('', views.choose_role, name='choose_role'),
]