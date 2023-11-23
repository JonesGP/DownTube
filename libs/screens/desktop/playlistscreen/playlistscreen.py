#Classes responsaveis pela tela de pesquisa
from kivymd.uix.screen import MDScreen
from pytube import YouTube
import time
import threading
from pathlib import Path
class PlayListScreen(MDScreen):
    pass

class MySearchPlaylist:
    def check_folder(self, app, checkbox, value):
        print(checkbox, value)
        app.createfolder = value
    def downallvideosplay(self, app, videosdown):
        quantdown =  app.get_running_app().root.ids.playlistscreentab.children[0].ids.quantdown
        app.downmultiplay = True
        if app.createfolder:
            app.pathsave
            folder_play = Path(app.pathsave, app.playlistvi.title)
            folder_play.mkdir(parents=True, exist_ok=True)
            folder_playlist_path = folder_play.resolve()
            print(folder_playlist_path)
        else:
            folder_playlist_path = ''
        for number, video in enumerate(videosdown):
            if number == 0:
                quantdown.text = f'{number}/{len(videosdown)}'
            video.register_on_progress_callback(app.on_progress)
            videostream = video.streams.get_highest_resolution()
            videoatual = app.downloadvideo(videostream, folder_playlist_path, None)
            quantdown.text = f'{number+1}/{len(videosdown)}'
        print('sai do downallvideosplay')
        app.downmultiplay = False
    # Função que pega as informações que o usuario digitou na tela com a quantidade de videos que ele quer baixar
    def download_playlist(self, app, opvideos):
        videosdown = []
        if '-' in opvideos:
            opvideos = opvideos.split("-")
            for opvideo in range(int(opvideos[0]), int(opvideos[1])+1):
                videosdown.append(app.searchclass.listvideosplay[int(opvideo)-1])
    
        elif ',' in opvideos:
            opvideos = opvideos.split(",")
            stativideo = int(opvideos[0])
            endvideo = int(opvideos[1])
            for video in range(stativideo, endvideo + 1):
                videosdown.append(app.searchclass.listvideosplay[int(video)-1])
                
        # Função para baixar todos os videos
        elif 'tudo todos' in opvideos:
            for video in app.searchclass.listvideosplay:
                videosdown.append(video)
        threading.Thread(target=self.downallvideosplay, args=(app, videosdown)).start()
        # Função para pega a lista videosdown e chama a função de download para cada video