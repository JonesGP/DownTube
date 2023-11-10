from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.image import AsyncImage
from pytube import Search
import threading
from kivy.clock import Clock
from pytube import Playlist
import time

from libs.functions.conversionsfuncs import ConversionsFuncs
global button
global listvideosplay
global listvideoob
listvideoob = []
listvideosplay = []

class SearchScreen(MDScreen):
    pass
     
class MySearchFunctions:
    def __init__(self) -> None:
        self.converfuncsclass = ConversionsFuncs()
        self.listvideosplay = listvideosplay
        
        # Função que cria os botões na tela
    def createboxvideos(self, app, boxvideossearch, video, videoitems, numindex):
        global listvideoob
        boxla = MDBoxLayout(orientation='horizontal', size_hint_y=None, size_hint_x=1, height=130, padding=5, spacing=5)
        if numindex != False:
            boxla.add_widget(MDLabel(text=str(numindex), text_color=app.theme_cls.text_color, size_hint=(0.05, None), height=130))
        boxla.add_widget(AsyncImage(source=videoitems[0], size_hint=(0.2, 1)))
                        
        boxinfo = MDBoxLayout(orientation='vertical', size_hint=(0.9, 1))
        boxinfo.add_widget(MDLabel(text=str(videoitems[1]), text_color=app.theme_cls.text_color, size_hint=(1, 0.4))) #titulo
            
        boxviewsage = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.09))
        boxviewsage.add_widget(MDLabel(text=f"{videoitems[2]} de vizualizações", font_size='1sp', text_color=app.theme_cls.text_color, size_hint=(0.7, 1))) #views
        boxviewsage.add_widget(MDLabel(text=f"há {videoitems[3]}",font_size='1sp', text_color=app.theme_cls.text_color, size_hint=(0.3, 1))) #data
        
        boxinfo.add_widget(boxviewsage)
        boxinfo.add_widget(MDLabel(text=str(videoitems[5]), text_color=app.theme_cls.text_color, size_hint=(1, 0.3))) #canal
        boxinfo.add_widget(MDLabel(text=str(videoitems[4]), text_color=app.theme_cls.text_color, size_hint=(1, 0.1))) #tempo
        boxla.add_widget(boxinfo)
        bottonn = MDIconButton(icon='download', size_hint=(None, None),pos_hint= {'center_x': 0.5,'center_y': 0.5}, md_bg_color= app.theme_cls.accent_color, on_release=lambda btn, video=video :app.searchclass.appatual(app, videoitems[6]))
        boxla.add_widget(bottonn)
        boxvideossearch.add_widget(boxla, index=numindex)
        
        # Recebe os dados, cria uma lista com varias informaçoes do video e agenda a execução de cada uma das funções de criação de botão na tela
    def pesquisarcomtheading(self, app, video, boxvideossearch, index):
        videoitems = []
        videoitems.append(video.thumbnail_url)
        videoitems.append(video.title)
        videoitems.append(self.converfuncsclass.viewsconv(video.views))
        videoitems.append(self.converfuncsclass.dateconv(video.publish_date))
        videoitems.append(self.converfuncsclass.formtimeseg(video.length))
        videoitems.append(video.author)
        videoitems.append(video.video_id)
        videoitems.append(index)
        Clock.schedule_once(lambda x: self.createboxvideos(app, boxvideossearch, video, videoitems, index), 0.01)
        
        # Função principal
        # Função que recebe o app, o texto de pesquisa e a caixa de videos. Com base nisso verifica se veio uma playlist ou não, executa a pesquisa ou cria a playlist
    def searchvideos(self,app, searchtext, boxvideossearch):
        boxvideossearch.clear_widgets()
        global listvideoob
        try: 
            if "https://" in searchtext:
                global listvideosplay
                self.listvideosplay = []
                playlistvi = Playlist(searchtext)
                app.get_running_app().root.ids.playlistscreentab.children[0].ids.nameplaylist.text = f'Nome da Playlist: {playlistvi.title}'
                app.get_running_app().root.ids.playlistscreentab.children[0].ids.lengthplaylist.text = f"Quantidade de videos: {playlistvi.length}"
                for index, video in enumerate(playlistvi.videos):
                    self.listvideosplay.append(video)
                    threading.Thread(target=self.pesquisarcomtheading, args=(app, video, boxvideossearch, index + 1)).start()
            else:
                sea = Search(searchtext)
                videosre = sea.results
                for video in videosre:
                    threading.Thread(target=self.pesquisarcomtheading, args=(app, video, boxvideossearch, False)).start()
        except Exception as error:
            app.get_running_app().show_alert_dialog(error)
        
    # Função que pega o id do video e envia para a tela de download e depois clica em confirmar para ve o video
    def appatual(self, app, videoid):
        app.get_running_app().root.switch_tab("home")
        linkvideo = f"https://www.youtube.com/watch?v={videoid}"
        print(linkvideo)
        app.get_running_app().confirm_link(linkvideo)
        
