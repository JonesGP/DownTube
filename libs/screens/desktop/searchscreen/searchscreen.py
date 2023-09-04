from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from pytube import Search
import threading
from kivymd.app import MDApp

from libs.functions.conversionsfuncs import ConversionsFuncs
global button
class SearchScreen(MDScreen):
    pass
     
class MySearchFunctions:
    def __init__(self) -> None:
        self.converfuncsclass = ConversionsFuncs()
        
        
    def searchvideos(self,app, text, boxvideossearch):
        sea = Search(text)
        boxvideossearch.clear_widgets()

        for video in sea.results:
            boxla = MDBoxLayout(orientation='horizontal', size_hint_y=None, size_hint_x=1, height=100, padding=5)
            boxla.add_widget(AsyncImage(source=video.thumbnail_url, size_hint=(0.3, 1)))
            
            boxinfo = MDBoxLayout(orientation='vertical', size_hint=(0.7, 1))
            boxinfo.add_widget(MDLabel(text=str(video.title), text_color=app.theme_cls.text_color, size_hint=(1, 0.4))) #titulo
            
            viewsformated = self.converfuncsclass.viewsconv(video.views)
            dateformated = self.converfuncsclass.dateconv(video.publish_date)
            boxviewsage = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.09))
            boxviewsage.add_widget(MDLabel(text=f"{viewsformated} de vizualizações",font_size=20, text_color=app.theme_cls.text_color, size_hint=(0.5, 1))) #views
            boxviewsage.add_widget(MDLabel(text=f"há {dateformated}", text_color=app.theme_cls.text_color, size_hint=(0.5, 1))) #data
            
            formated_time = self.converfuncsclass.formtimeseg(video.length)
            boxinfo.add_widget(boxviewsage)
            boxinfo.add_widget(MDLabel(text=str(video.author), text_color=app.theme_cls.text_color, size_hint=(1, 0.3))) #canal
            boxinfo.add_widget(MDLabel(text=str(formated_time), text_color=app.theme_cls.text_color, size_hint=(1, 0.1))) #tempo
            boxla.add_widget(boxinfo)
            bottonn = MDRaisedButton(text="Download", size_hint=(0.1, None), md_bg_color= app.theme_cls.primary_color, on_release=lambda btn, video=video :app.searchclass.appatual(app, video))
            boxla.add_widget(bottonn)
            boxvideossearch.add_widget(boxla)
    def appatual(self, app, video):
        app.get_running_app().root.switch_tab("home")
        print(app.get_running_app().confirm_link(video))
        
            
    pass