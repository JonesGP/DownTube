#Classes responsaveis pela tela de pesquisa
from kivymd.uix.screen import MDScreen
from pytube import YouTube
import time
import threading
class PlayListScreen(MDScreen):
    pass

class MySearchPlaylist:
    def downallvideosplay(self, app, videosdown):
        for video in videosdown:
            video.register_on_progress_callback(app.on_progress)
            videostream = video.streams.get_highest_resolution()
            videoatual = app.downloadvideo(videostream, '', None)
    # Função que pega as informações que o usuario digitou na tela com a quantidade de videos que ele quer baixar
    def download_playlist(self, app, opvideos):
        videosdown = []
        if '-' in opvideos:
            opvideos = opvideos.split("-")
            print(opvideos)
            for opvideo in range(int(opvideos[0]), int(opvideos[1])):
                print(app.searchclass.listvideosplay[int(opvideo)-1])
                videosdown.append(app.searchclass.listvideosplay[int(opvideo)-1])
    
        elif ',' in opvideos:
            opvideos = opvideos.split(",")
            stativideo = int(opvideos[0])
            endvideo = int(opvideos[1])
            for video in range(stativideo, endvideo + 1):
                print(app.searchclass.listvideosplay[int(video)-1])
                videosdown.append(app.searchclass.listvideosplay[int(video)-1])
                
        # Função para baixar todos os videos
        elif 'tudo todos' in opvideos:
            for video in app.searchclass.listvideosplay:
                videosdown.append(video)
        threading.Thread(target=self.downallvideosplay, args=(app, videosdown)).start()
        # Função para pega a lista videosdown e chama a função de download para cada video