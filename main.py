from pytube import YouTube
from pathlib import Path
import threading

from typing import BinaryIO
from kivymd.app import MDApp
from kivy.core.window import Window
from libs.screens.home import Home
from kivy.lang.builder import Builder
from kivymd.uix.button import MDRaisedButton

videosob = []
resolutionslist = []
pathsave = ""
jachamado = False
tamanhototal = 0
progressbardown1 = None
class DownTube(MDApp):

    def confirm_link(self, text, imagevideo, titlevideo, sizevideo, boxdownloads, pathsave, progressbardown):
        yt = YouTube(text)
        global progressbardown1
        progressbardown1 = progressbardown
        pathsave = pathsave
        imagevideo.source = yt.thumbnail_url
        titlevideo.text = yt.title
        #tempo do video 
        segundos = yt.length
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        formated_time = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        sizevideo.text = str(formated_time)
        boxdownloads.clear_widgets()
        for video in yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution'):
            videosob.append(video)
            resolutionslist.append(video.resolution)
            buttonraised = MDRaisedButton(text=f"{video.resolution} {str(int(video.filesize_mb))}MB", on_release=self.create_button_callback(video, pathsave))
            boxdownloads.add_widget(buttonraised)
    
    def create_button_callback(self, video, pathsave):
        return lambda x: self.downloadvideo(video, pathsave)

    def on_progress(self, chunk: bytes, file_handler: BinaryIO, bytes_remaining: int):
        """On progress callback function.

        This function writes the binary data to the file, then checks if an
        additional callback is defined in the monostate. This is exposed to
        allow things like displaying a progress bar.

        :param bytes chunk:
            Segment of media file binary data, not yet written to disk.
        :param file_handler:
            The file handle where the media is being written to.
        :type file_handler:
            :py:class:`io.BufferedWriter`
        :param int bytes_remaining:
            The delta between the total file size in bytes and amount already
            downloaded.

        :rtype: None
        
        """
        self.progress_bar_download(bytes_remaining)
        file_handler.write(chunk)
        
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
        video.on_progress = self.on_progress
        if pathsave == "":
            pathsave = Path.home() / "Downloads"
        video.download(pathsave)

    def build(self, **kwargs):
        Window.size = [720,600]
        self.load_all_kv_files()
        self.title = "DownTube - Developed by JonesGP"
        return Home()
    
    def load_all_kv_files(self):
        Builder.load_file('libs/screens/home.kv')
    
if __name__ == "__main__":
    DownTube().run()