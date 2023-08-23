from pytube import YouTube
from pathlib import Path
import threading

from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.home import Home
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRaisedButton

videosob = []
resolutionslist = []
pathsave = None
videostream = None
class DownTube(MDApp):

    def confirm_link(self, text, imagevideo, titlevideo, sizevideo, boxdownloads ):
        yt = YouTube(text)
        pathsave = text
        imagevideo.source = yt.thumbnail_url
        titlevideo.text = yt.title
        #tempo do video 
        segundos = yt.length
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        formated_time = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        sizevideo.text = str(formated_time)
        
        for video in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
            videosob.append(video)
            resolutionslist.append(video.resolution)
            buttonraised = MDRaisedButton(text=f"{video.resolution} {str(video.filesize_mb)}mb", on_release=self.create_button_callback(video))
            boxdownloads.add_widget(buttonraised)
    
    def create_button_callback(self, video):
        return lambda x: self.downloadvideo(video, pathsave)

    def on_progress(self, chunk, file_handle, bytes_remaining):
        donwloadeadbytes = bytes_remaining / 1000000
        print(f"Downloaded {donwloadeadbytes}")
        
    
    def downloadvideo(self, video, pathsave):
        threading.Thread(target=self.funçao_download, args=(video, pathsave)).start()

    def funçao_download(self, video, pathsave):
        videostream = video
        video.on_progress = self.on_progress
        video.download(pathsave)

    def build(self, **kwargs):
        Window.size = [720,600]
        self.load_all_kv_files()
        return Home()
    
    def load_all_kv_files(self):
        Builder.load_file('libs/screens/home.kv')
    
if __name__ == "__main__":
    DownTube().run()