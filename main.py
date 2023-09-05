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
        imagevideo = widgetsdownloadscreen[3]
        titlevideo = widgetsdownloadscreen[5]
        sizevideo = widgetsdownloadscreen[6]
        chanelvideo = widgetsdownloadscreen[7]
        boxdownloads = widgetsdownloadscreen[8]
        progressbardown = widgetsdownloadscreen[9]
        pathsave = widgetsdownloadscreen[10].text

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
        boxdownloads.add_widget(MDRaisedButton(text=f"{yt.streams.filter(only_audio=True).order_by('abr').last().subtype} {str(int(yt.streams.filter(only_audio=True).order_by('abr').last().filesize_mb))}MB", on_release=self.create_button_callback(yt.streams.filter(only_audio=True).order_by('abr').last(), pathsave)))
     
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

    def funçao_download(self, video, pathsave):
        global jachamado
        global tamanhototal
        jachamado = False
        tamanhototal = 0
        if pathsave == "":
            pathsave = Path.home() / "Downloads"
        video.download(pathsave)

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