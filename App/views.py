from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import VideoDownload, VideoPlayer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required, user_passes_test

def handler404(request, exception):
     return render(request, 'pagina_nao_encontrada.html', status=404)

def main(request):
    return redirect(login)

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = User.objects.filter(username=request.POST.get('nomeusuario')).first()
        email = User.objects.filter(email=request.POST.get('nomeusuario')).first()
        senha = User.objects.filter(password=request.POST.get('senha')).first()
        if email == None and username == None:
            return HttpResponse('Usuário incorreto. Favor tente novamente ou efetue um novo cadastro.')
        user = authenticate(username=request.POST.get('nomeusuario'), password=request.POST.get('senha'))
        if not user:
            return HttpResponse('Senha incorretos. Favor tente novamente.')
        login_django(request, user)
                
        return redirect(home)

@login_required(login_url='/tubepobre/login/')
def logout(request):
    logout_django(request)
    return redirect(login)

@login_required(login_url='/tubepobre/login/')
def home(request):
    usuario = request.user.username
    arquivos = VideoPlayer.listar_videos(usuario)
    caminho = arquivos[0]
    audios = arquivos[1]
    usuario_espaco = list()
    usuario_espaco.append(round(VideoDownload.usuario_espaco_disponivel(usuario) / (1024 * 1024), 2))
    usuario_espaco.append(round(1048576*64 / (1024 * 1024), 2))
    porcentagem_amazenamento = round(usuario_espaco[0]/usuario_espaco[1] * 100, 2)

    return  render(request, 'index.html', {'caminho': caminho, "audios": audios, "usuario_espaco":usuario_espaco, "porcentagem_amazenamento":porcentagem_amazenamento})

@login_required(login_url='/tubepobre/login/')
def busca(request):
    url_video = request.POST.get('url_video')
    print(url_video)
    if url_video == None or url_video == "":
        return redirect(home)
    resolucoes, extensoes_video, extensoes_audio, tamanhos_videos, tamanhos_audios, titulo = VideoDownload.buscar(url_video)

    return render(request, 'busca.html', {"resolucoes":resolucoes, "extensoes_video":extensoes_video, "extensoes_audio":extensoes_audio, "tamanhos_videos":tamanhos_videos, "tamanhos_audios":tamanhos_audios, "titulo":titulo, "url_video":url_video})

@login_required(login_url='/tubepobre/login/')
def download_audio(request, itag: int, url_video: str):
    usuario_nome = request.user.username
    VideoDownload.download_audio(url_video, itag, usuario_nome)

    return redirect(home)

@login_required(login_url='/tubepobre/login/')
def download_video(request, resolucao: int, url_video: str):
    usuario_nome = request.user.username
    VideoDownload.download_video(url_video, resolucao, usuario_nome)

    return redirect(home)

@login_required(login_url='/tubepobre/login/')
def excluir_download(request, nome_download):
    VideoDownload.excluir_download(request.user.username, nome_download, False)
    return redirect(home)