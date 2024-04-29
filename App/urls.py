from django.contrib import admin
from django.urls import path
from . import views
import string

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('tubepobre/login/', views.login, name="login"),
    path('tubepobre/home/logout/', views.logout, name="logout"),
    path('tubepobre/home/', views.home, name='home'),
    path('tubepobre/home/busca/', views.busca, name='busca'),
    path('tubepobre/home/busca/download_video/<int:resolucao>/<path:url_video>/', views.download_video, name='download_video'),
    path('tubepobre/home/busca/download_audio/<str:itag>/<path:url_video>/', views.download_audio, name='download_audio'),
    path('tubepobre/home/excluir_download/<str:nome_download>/', views.excluir_download, name='excluir_download'),
]

handler404 = "App.views.handler404"