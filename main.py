from pytube import YouTube
from pathlib import Path
import threading
import logging
logging.raiseExceptions = False
from typing import BinaryIO
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRaisedButton
from kivy.config import Config

from libs.screens.home import Home
from libs.screens.desktop.searchscreen.searchscreen import MySearchFunctions
from libs.functions.conversionsfuncs import ConversionsFuncs
import requests
import unicodedata
from ffprobe import FFProbe
import subprocess
import re

ffmpeg_path = r'.\libs\ffmpeg\bin\ffmpeg.exe'
ffprobedir = r'.\libs\ffmpeg\bin\ffprobe.exe'
versaoapp = "v0.3.0-alpha"

Config.set('kivy', 'window_icon', 'icon.ico')
Window.set_icon("icon.ico")
videosob = []
resolutionslist = []
pathsave = ""
jachamado = False
tamanhototal = 0
progressbardown1 = None
themedark = False
class DownTube(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.searchclass = MySearchFunctions()
        self.converfuncsclass = ConversionsFuncs()
        self.home = Home()
        
        
    def versao_atual(self):
        global versaoapp
        return f"Versão app: {versaoapp}"
    def pegar_ultima_versao(self):
        global versaoapp
        try:
            user_name = "jonesgp"
            repor_name = "downtube"
            url_repo = f"https://api.github.com/repos/{user_name}/{repor_name}/tags"
            resposta = requests.get(url_repo)
            if resposta.status_code == 200:
                tags = resposta.json()
                if tags:
                    lastest_tag = tags[0]["name"]
                    if versaoapp != lastest_tag:
                        textvergit = f"Há uma nova versão disponível: {lastest_tag}"
                    elif versaoapp == lastest_tag:
                        textvergit = f"Você está usando a última versão: {lastest_tag}"
                    if textvergit != None:
                        return textvergit
        except:
            return f"Não foi possível obter a última versão"
        return f"Versão atual: {versaoapp}"
    def theme_button(self):
        global themedark
        if not themedark:
            themedark = True
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "BlueGray"
            self.theme_cls.accent_palette = "Teal"
        else:
            themedark = False
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "LightBlue"
            self.theme_cls.accent_palette = "Teal"
    def confirm_link(self, linkvideo):
        widgetsdownloadscreen = []
        for item in self.root.ids.hometab.children[0].ids:
            widgetsdownloadscreen.append(getattr(self.root.ids.hometab.children[0].ids, item))
            print(item)
        imagevideo = widgetsdownloadscreen[5]
        titlevideo = widgetsdownloadscreen[7]
        sizevideo = widgetsdownloadscreen[8]
        chanelvideo = widgetsdownloadscreen[9]
        boxdownloads = widgetsdownloadscreen[10]
        progressbardown = widgetsdownloadscreen[11]
        pathsave = widgetsdownloadscreen[13].text

        try:
            if type(linkvideo) == str:
                yt = YouTube(linkvideo)
            elif type(linkvideo) == YouTube:
                yt = linkvideo  
        except:
            return
        global progressbardown1
        yt.register_on_progress_callback(self.on_progress)
        progressbardown1 = progressbardown
        pathsave = pathsave
        imagevideo.source = yt.thumbnail_url
        titlevideo.text = f"Titulo: {yt.title}"
        chanelvideo.text = f"Canal: {yt.author}"
        #tempo do video
        formated_time = self.converfuncsclass.formtimeseg(yt.length)
        sizevideo.text = f"Tempo: {str(formated_time)}"
        boxdownloads.clear_widgets()
        for video in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
            videosob.append(video)
            resolutionslist.append(video.resolution)
            buttonraised = MDRaisedButton(text=f"{video.resolution} {str(int(video.filesize_mb))}MB", on_release=self.create_button_callback(video, pathsave))
            boxdownloads.add_widget(buttonraised)
        #Botão Audio yt.streams.filter(only_audio=True).order_by('abr').last().subtype
        boxdownloads.add_widget(MDRaisedButton(text=f"MP3 {str(int(yt.streams.filter(only_audio=True).order_by('abr').last().filesize_mb))}MB", on_release=self.create_button_callback(yt.streams.filter(only_audio=True).order_by('abr').last(), pathsave)))
     
    def conver_audio(self, audio_file,output_file, output_format):
        def monitorar_progresso(comando):
            processo = subprocess.Popen(comando, shell=False, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)

            duracao_total = None

            # Regex para extrair a duração total do stderr do FFmpeg
            regex_duracao = r"Duration: (\d{2}):(\d{2}):(\d{2})"

            while True:
                output = processo.stderr.readline().strip()

                if output:
                    duracao_match = re.search(regex_duracao, output)
                    if duracao_match:
                        duracao_total = int(duracao_match.group(1))*3600 + int(duracao_match.group(2))*60 + int(duracao_match.group(3))

                    tempo_match = re.search(r"time=(\d{2}):(\d{2}):(\d{2})", output)
                    if tempo_match and duracao_total:
                        tempo_atual = int(tempo_match.group(1))*3600 + int(tempo_match.group(2))*60 + int(tempo_match.group(3))
                        progresso = (tempo_atual / duracao_total) * 100
                        print(f"Progresso da conversão: {progresso:.2f}%")
                        progressbarconv = getattr(self.root.ids.hometab.children[0].ids, "progressbardown")
                        statusok = getattr(self.root.ids.hometab.children[0].ids, "statusok")
                        statusok.text = f"Convertendo {progresso:.0f}%"
                        progressbarconv.value = progresso
                        

                if processo.poll() is not None:
                    statusok.text = "Conversão concluída!"
                    break

            if processo.returncode == 0:
                print("Conversão concluída com sucesso!")
            else:
                print("Ocorreu um erro durante a conversão.")
        command = [ffmpeg_path, '-i', audio_file, '-ab', '128k', '-ac', '2', '-ar', '44100', '-y', output_file]
        monitorar_progresso(command)
    def create_button_callback(self, video, pathsave):
        return lambda x: self.downloadvideo(video, pathsave)

    def on_progress(self, chunk: bytes, file_handler: BinaryIO, bytes_remaining: int):
        self.progress_bar_download(bytes_remaining)
        
    def progress_bar_download(self, bytes_remaining, **kwargs):
        global jachamado
        global tamanhototal
        global progressbardown1
        porcentagem = 0
        if not jachamado:
            tamanhototal = bytes_remaining
            jachamado = True
        try:
            porcentagem = 100 - (bytes_remaining / tamanhototal) * 100
            progressbardown1.value = porcentagem
        except:
            pass

    def downloadvideo(self, video, pathsave):
        threading.Thread(target=self.funçao_download, args=(video, pathsave)).start()

        print(video)

    def funçao_download(self, video, pathsave):
        global jachamado
        global tamanhototal
        jachamado = False
        tamanhototal = 0
        if pathsave == "":
            pathsave = Path.home() / "Downloads"
        statusok = getattr(self.root.ids.hometab.children[0].ids, 'statusok')
        statusok.text = 'Baixando...'
        video.download(pathsave)
        statusok.text = 'Baixado!'
        if video.type == "audio":
            caminhoarq = f"{video.download(pathsave)}"
            self.conver_audio(caminhoarq, caminhoarq.replace(".webm", ".mp3"), 'mp3')
            Path(caminhoarq).unlink()
        

    def build(self, **kwargs):
        Window.minimum_height = 599
        Window.minimum_width = 799
        Window.icon = "icon.ico"
        Window.set_icon("icon.ico")
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.accent_palette = "Blue"
        self.theme_cls.theme_style_switch_animation = True
        self.load_all_kv_files()
        self.title = "DownTube - Developed by JonesGP"
        return Builder.load_file('libs/screens/home.kv')
    
    def load_all_kv_files(self):
        pass
    
mysearchfunctions = MySearchFunctions()
if __name__ == "__main__":
    DownTube().run()