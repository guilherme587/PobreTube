from typing import Iterable
from django.db import models
import os
from pytube import YouTube
from . import settings

class VideoDownload():
    @staticmethod
    def download_video(url:str, resolucao:str, user_name:str):
        resolucao = (str(resolucao) + "p")
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension="mp4", resolution=resolucao).first()
        if stream == None:
            stream = yt.streams.filter(progressive=True, resolution=resolucao).first()
        caminho = str(settings.STATIC_URL) + "downloads/" + str(user_name)
        if not VideoDownload.espaco_disponivel(caminho, stream.filesize) and user_name != "admin":
            return False
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        stream.download(output_path=str(caminho))

    @staticmethod
    def download_audio(url:str, itag:str, user_name:str):
        yt = YouTube(url)
        audio_stream = yt.streams.get_by_itag(itag)
        caminho = str(settings.STATIC_URL) + "downloads/" + str(user_name)
        if not VideoDownload.espaco_disponivel(caminho, audio_stream.filesize) and user_name != "admin":
            return False
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        audio_stream.download(output_path=str(caminho))
    
    @staticmethod
    def buscar(url:str):
        video = YouTube(url)
        resolucoes = VideoDownload.listar_resolucoes_disponiveis(video)
        extensoes_video = VideoDownload.listar_extensoes_disponiveis_video(video)
        extensoes_audio = VideoDownload.listar_extensoes_disponiveis_audio(video)
        titulo = video.title
        tamanhos_videos = list()
        tamanhos_audios = list()
        streams = video.streams.filter(progressive=True)
        for stream in streams:
            for resolucao in resolucoes:
                if stream.resolution == (str(resolucao[0])+"p"):
                        tamanhos_videos.append(round(stream.filesize / (1024 * 1024), 2))
                        break
        streams = video.streams.filter(only_audio=True)
        for stream in streams:
            for extensao in extensoes_audio:
                if stream.itag == extensao.itag:
                        tamanhos_audios.append(round(stream.filesize / (1024 * 1024), 2))
                        break

        return resolucoes, extensoes_video, extensoes_audio, tamanhos_videos, tamanhos_audios, titulo
    
    @staticmethod
    def espaco_disponivel(caminho:str, stream_tamanho: float):
        tamanho_total = 0
        for arquivo in os.listdir(caminho):
            caminho_arquivo = os.path.join(caminho, arquivo)
            if os.path.isfile(caminho_arquivo):
                tamanho_total += os.path.getsize(caminho_arquivo)

        if (tamanho_total + stream_tamanho) >= 1048576*64:
            return False
        return True
    
    @staticmethod
    def usuario_espaco_disponivel(nome_usuario:str):
        caminho = str(settings.STATIC_URL) + "downloads/" + str(nome_usuario)
        tamanho_total = 0
        for arquivo in os.listdir(caminho):
            caminho_arquivo = os.path.join(caminho, arquivo)
            if os.path.isfile(caminho_arquivo):
                tamanho_total += os.path.getsize(caminho_arquivo)

        return tamanho_total

    @staticmethod
    def listar_resolucoes_disponiveis(video:YouTube):
        streams = video.streams.filter(progressive=True)
        resolucoes_disponiveis = [[stream.resolution, stream.bitrate] for stream in streams]
        for resolucao in resolucoes_disponiveis:
            resolucoes_disponiveis[resolucoes_disponiveis.index(resolucao)] = [int(resolucao[0].replace('p', '')), resolucao[1]]

        return resolucoes_disponiveis
    
    @staticmethod
    def listar_extensoes_disponiveis_video(video:YouTube):
        streams = video.streams.all()
        extensoes = set()
        for stream in streams:
            if stream.includes_video_track:
                extensoes.add(stream.mime_type.split("/")[1])

        return extensoes
    
    @staticmethod
    def listar_extensoes_disponiveis_audio(video:YouTube):
        return video.streams.filter(only_audio=True)
    
    @staticmethod
    def baixar(url:str):
        resolucao = VideoDownload.listar_resolucoes_disponiveis(url)
        VideoDownload.play_youtube_video(url, resolucao[-1])
    
    @staticmethod
    def excluir_download(nome_usuario:str, nome_download:str, excluir:bool = False) -> (str|None):
        caminho = str(settings.STATIC_URL) + "downloads/" + str(nome_usuario) + "/" + str(nome_download)
        if os.path.exists(caminho):
            os.remove(caminho)
        else:
            return f"Caminho ou arquivo para {nome_download} não existem."

class VideoPlayer():
    @staticmethod
    def listar_videos(usuario_nome:str) -> list:
        caminho = str(settings.STATIC_URL) + "downloads/" + str(usuario_nome)
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        arquivos = []
        arquivos.append(caminho[7:] + str("/"))
        arquivos.append(os.listdir(caminho))

        return arquivos