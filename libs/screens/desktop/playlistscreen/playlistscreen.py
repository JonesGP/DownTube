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
    def select_resolution_playlist(self, app, checkbox, value):
        if checkbox == app.get_running_app().root.ids.playlistscreentab.children[0].ids.check720p and value == True:
            app.get_running_app().root.ids.playlistscreentab.children[0].ids.check1080p.active = False
            app.selecresolutionplaylist = '720p'
        elif checkbox == app.get_running_app().root.ids.playlistscreentab.children[0].ids.check1080p and value == True:
            app.get_running_app().root.ids.playlistscreentab.children[0].ids.check720p.active = False
            app.selecresolutionplaylist = '1080p'
        else:
            app.selecresolutionplaylist = '720p'
        print(app.selecresolutionplaylist)
    def downallvideosplay(self, app, videosdown):
        quantdown =  app.get_running_app().root.ids.playlistscreentab.children[0].ids.quantdown
        app.downmultiplay = True
        
        if app.createfolder:
            if app.get_running_app().root.ids.playlistscreentab.children[0].ids.namefolderuserplaylist.text != '':
                folder_play = Path(app.pathsave, app.get_running_app().root.ids.playlistscreentab.children[0].ids.namefolderuserplaylist.text)
                folder_play.mkdir(parents=True, exist_ok=True)
                folder_playlist_path = folder_play.resolve()
            else:
                folder_play = Path(app.pathsave, app.playlistvi.title)
                folder_play.mkdir(parents=True, exist_ok=True)
                folder_playlist_path = folder_play.resolve()

            app.pathsave = folder_playlist_path
        else:
            folder_playlist_path = ''
        for number, video in enumerate(videosdown):
            if number == 0:
                quantdown.text = f'{number}/{len(videosdown)}'
            video.register_on_progress_callback(app.on_progress)
            if app.selecresolutionplaylist == '720p':
                videostream = video.streams.get_highest_resolution()
                audiostream = None
            elif app.selecresolutionplaylist == '1080p':
                videostream = video.streams.filter(res='1080p', file_extension='webm').last()
                audiostream = video.streams.filter(only_audio=True).order_by('abr').last()
            if videostream is None:
                videostream = video.streams.get_highest_resolution()
                audiostream = None
            videoatual = app.downloadvideo(videostream, folder_playlist_path, audiostream)
            quantdown.text = f'{number+1}/{len(videosdown)}'
        app.downmultiplay = False
        app.pathsave = app.pathsavedefault
    # Função que pega as informações que o usuario digitou na tela com a quantidade de videos que ele quer baixar
    def download_playlist(self, app, opvideos):
        if opvideos == '':
            app.show_alert_dialog('Nenhum video selecionado')
            return
        videosdown = []
        if '-' in opvideos:
            opvideos = opvideos.split("-")
            for opvideo in range(int(opvideos[0]), int(opvideos[1])+1):
                videosdown.append(app.searchclass.listvideosplay[int(opvideo)-1])
    
        elif ',' in opvideos:
            opvideos = opvideos.split(",")
            for video in opvideos:
                videosdown.append(app.searchclass.listvideosplay[int(video)-1])
                
        # Função para baixar todos os videos
        elif 'tudo todos' in opvideos:
            for video in app.searchclass.listvideosplay:
                videosdown.append(video)
        else:
            videosdown.append(app.searchclass.listvideosplay[int(opvideos)-1])
        threading.Thread(target=self.downallvideosplay, args=(app, videosdown)).start()
        # Função para pega a lista videosdown e chama a função de download para cada video