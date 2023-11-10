from kivymd.uix.screen import MDScreen
from pytube import YouTube
class PlayListScreen(MDScreen):
    pass

class MySearchPlaylist:
    # Função que pega as informações que o usuario digitou na tela com a quantidade de videos que ele quer baixar
    def download_playlist(self, app, opvideos):
        videosdown = []
        if '-' in opvideos:
            opvideos = opvideos.split("-")
            for opvideo in opvideos:
                print(app.searchclass.listvideosplay[int(opvideo)-1])
                videosdown.append(app.searchclass.listvideosplay[int(opvideo)-1])
        elif ',' in opvideos:
            opvideos = opvideos.split(",")
            stativideo = int(opvideos[0])
            endvideo = int(opvideos[1])
            for video in range(stativideo, endvideo + 1):
                print(app.searchclass.listvideosplay[int(video)-1])
                videosdown.append(app.searchclass.listvideosplay[int(video)-1])
        for video in videosdown:
            video.register_on_progress_callback(app.on_progress)
            videostream = video.streams.get_highest_resolution()
            app.downloadvideo(videostream, '')