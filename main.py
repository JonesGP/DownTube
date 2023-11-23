from pytube import YouTube
from pytube import Playlist
from pathlib import Path
import threading
import logging
logging.raiseExceptions = False
from typing import BinaryIO
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.config import Config
from kivymd.theming import ThemeManager
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp


from libs.screens.home import Home
from libs.screens.desktop.searchscreen.searchscreen import MySearchFunctions
from libs.functions.conversionsfuncs import ConversionsFuncs
from libs.screens.desktop.playlistscreen.playlistscreen import MySearchPlaylist
import requests
import unicodedata
import subprocess
import re
import os
import time

global MODODESENVOLVIMENTO
MODODESENVOLVIMENTO = True

ffmpeg_path = r'.\libs\ffmpeg\bin\ffmpeg.exe'
ffprobedir = r'.\libs\ffmpeg\bin\ffprobe.exe'
versaoapp = "v0.4.0-alpha"


Config.set('kivy', 'window_icon', 'icon.ico')
Window.set_icon("icon.ico")
Window.minimum_height = 599
Window.minimum_width = 799
videosob: list[str] = []
resolutionslist: list[str] = []
pathsave = Path.home() / "Downloads"
jachamado = False
tamanhototal = 0
progressbardown1 = None
themedark = False
downmultiplay = False #variavel que define se vai ser download de um video ou de uma playlist
createfolder = False #variavel que define se vai ser criado uma pasta com da playlist

class DownTube(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.searchclass = MySearchFunctions()
        self.converfuncsclass = ConversionsFuncs()
        self.searchplaylist = MySearchPlaylist()
        self.home = Home()
        self.dialog = None
        self.downmultiplay = downmultiplay
        self.createfolder = createfolder
        self.playlistvi = None
        self.pathsave = pathsave
    def versao_atual(self):
        global versaoapp
        return f"Versão app: {versaoapp}"
    
    def pegar_ultima_versao(self):
        global versaoapp
        if MODODESENVOLVIMENTO:
            return f"Versão atual: {versaoapp}"
        textvergit = None
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
        global progressbardown1
        widgetsdownloadscreen = []
        for item in self.root.ids.hometab.children[0].ids:
            widgetsdownloadscreen.append(getattr(self.root.ids.hometab.children[0].ids, item))
        imagevideo = widgetsdownloadscreen[5]
        titlevideo = widgetsdownloadscreen[7]
        sizevideo = widgetsdownloadscreen[8]
        chanelvideo = widgetsdownloadscreen[9]
        boxdownloads = widgetsdownloadscreen[10]
        progressbardown = widgetsdownloadscreen[11]
        pathsave = widgetsdownloadscreen[13].text

        try:
            if type(linkvideo) == str:
                print('teste 1')
                yt = YouTube(linkvideo)
            elif type(linkvideo) == YouTube:
                print('teste 2')
                yt = linkvideo 
                
        except:
            self.show_alert_dialog('')
            return
        yt.register_on_progress_callback(self.on_progress)
        progressbardown1 = progressbardown
        imagevideo.source = yt.thumbnail_url
        titlevideo.text = f"Titulo: {yt.title}"
        chanelvideo.text = f"Canal: {yt.author}"
        #tempo do video
        formated_time = self.converfuncsclass.formtimeseg(yt.length)
        sizevideo.text = f"Tempo: {str(formated_time)}"
        boxdownloads.clear_widgets()
        try:
            for vi in yt.streams:
                print(vi)
            for video in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
                videosob.append(video)
                resolutionslist.append(video.resolution)
                buttonraised = MDRaisedButton(text=f"{video.resolution} {str(int(video.filesize_mb))}MB", on_release=self.create_button_callback(video, pathsave, None))
                boxdownloads.add_widget(buttonraised)
            for video in yt.streams.filter(res='1080p', file_extension='webm'):
                buttonraised = MDRaisedButton(text=f"{video.resolution} {str(int(video.filesize_mb))}MB", on_release=self.create_button_callback(video, pathsave, yt.streams.filter(only_audio=True).order_by('abr').last()))
                boxdownloads.add_widget(buttonraised)
            #Botão Audio yt.streams.filter(only_audio=True).order_by('abr').last().subtype
            boxdownloads.add_widget(MDRaisedButton(text=f"MP3 {str(int(yt.streams.filter(only_audio=True).order_by('abr').last().filesize_mb))}MB", on_release=self.create_button_callback(yt.streams.filter(only_audio=True).order_by('abr').last(), pathsave, None)))
        except Exception as error:
            self.show_alert_dialog('')
            return
        
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
    
    def join_video_audio(self, video_file, audio_file, output_file):
        command = f'{ffmpeg_path} -i "{video_file}" -i "{audio_file}" -c copy "{output_file}"'
        os.system(command)

    def create_button_callback(self, video, pathsave, audio):
        return lambda x: self.downloadvideo(video, pathsave, audio)

    def on_progress(self, chunk: bytes, file_handler: BinaryIO, bytes_remaining: int):
        self.progress_bar_download(bytes_remaining)
        
    def progress_bar_download(self, bytes_remaining, **kwargs):
        global jachamado
        global tamanhototal
        global progressbardown1
        porcentagem = 0
        if self.downmultiplay:
            progressbarplaylist = self.get_running_app().root.ids.playlistscreentab.children[0].ids.progressbarplaylist
            if not jachamado:
                tamanhototal = bytes_remaining
                jachamado = True
            try:
                porcentagem = 100 - (bytes_remaining / tamanhototal) * 100
                progressbarplaylist.value = porcentagem
            except:
                pass
            return
        if not jachamado:
            tamanhototal = bytes_remaining
            jachamado = True
        try:
            porcentagem = 100 - (bytes_remaining / tamanhototal) * 100
            progressbardown1.value = porcentagem
        except:
            pass

    def downloadvideo(self, video, pathsave, audio):
        downthread = threading.Thread(target=self.funçao_download, args=(video, pathsave, audio))
        downthread.start()
        while downthread.is_alive():
            time.sleep(1)
        return 'baixei'

    def funçao_download(self, video, pathsave, audio):
        global jachamado
        global tamanhototal
        jachamado = False
        tamanhototal = 0
        if pathsave == "":
            pathsave = Path.home() / "Downloads"
        statusok = getattr(self.root.ids.hometab.children[0].ids, 'statusok')
        statusok.text = 'Baixando...'
        print(video)
        video.download(pathsave)
        if audio != None:
            def editar_nome_arquivo(caminho_arquivo, novo_nome):
                # Cria um objeto Path a partir do caminho do arquivo
                path_arquivo = Path(caminho_arquivo)

                # Obtém o diretório e o nome do arquivo atual
                diretorio = path_arquivo.parent
                nome_arquivo = path_arquivo.name

                # Concatena o novo nome do arquivo com o diretório
                novo_caminho_arquivo = diretorio / novo_nome

                # Renomeia o arquivo
                path_arquivo.rename(novo_caminho_arquivo)
            editar_nome_arquivo(f'{pathsave}\{video.default_filename}', f'video{video.default_filename}')
            audio.download(pathsave)
            print(pathsave)
            
            video_file = f'{pathsave}\\video{video.default_filename}'
            audio_file = f'{pathsave}\{audio.default_filename}'
            output_file = f'{pathsave}\{video.default_filename.replace(".webm", ".mp4")}'
            # Comando FFmpeg para juntar o áudio e o vídeo
            statusok.text = 'Convertendo...'
            self.join_video_audio(video_file, audio_file, output_file)
            os.remove(video_file)
            os.remove(audio_file)
            
        statusok.text = 'Baixado!'
        if video.type == "audio":
            caminhoarq = f"{video.download(pathsave)}"
            self.conver_audio(caminhoarq, caminhoarq.replace(".webm", ".mp3"), 'mp3')
            Path(caminhoarq).unlink()
        return 'Registrado'
    
    def show_alert_dialog(self, error):
        if not self.dialog:
            self.dialog = MDDialog(
                text="O link não é valido ou o servidor está indisponível",
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Pesquisar no youtube",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
        self.dialog.open()
    
    def build(self, **kwargs):
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