from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.projects, name='projects'),
    path('news_feed/', views.news_feed, name='news_feed'),
    path('shop/', views.shop, name='shop'),
    path('add-useful-link/', views.add_useful_link, name='add-useful-link'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create-project/', views.create_project, name='create-project'),
    path('upload_photo/', views.upload_photo, name='upload_photo'),
    path('upload-video/', views.upload_video, name='upload_video'),
    path('add_content/', views.add_content, name='add_content'),
    path('update-project/<str:pk>', views.update_project, name='update-project'),
    path('update-video/<str:pk>', views.update_video, name='update-video'),
    path('update-photo/<str:pk>', views.update_photo, name='update-photo'),
    path('delete-project/<str:pk>', views.delete_project, name='delete-project'),
    path('delete-video/<str:pk>', views.delete_video, name='delete-video'),
    path('delete-photo/<str:pk>', views.delete_photo, name='delete-photo'),
    path('like_project/<int:project_id>/', views.like_project, name='like_project'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)