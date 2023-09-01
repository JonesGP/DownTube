from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from pytube import Search
import threading

from libs.functions.conversionsfuncs import ConversionsFuncs
class SearchScreen(MDScreen):
    pass
    
class MySearchFunctions:
    def __init__(self) -> None:
        self.converfuncsclass = ConversionsFuncs()
        
    def searchvideos(self, text, boxvideossearch):
        sea = Search(text)
        for video in sea.results:
            print(video.title)
            boxla = MDBoxLayout(orientation='horizontal', size_hint_y=None, size_hint_x=1, height=100, padding=5)
            boxla.add_widget(AsyncImage(source=video.thumbnail_url, size_hint=(0.3, 1)))
            
            boxinfo = MDBoxLayout(orientation='vertical', size_hint=(0.7, 1))
            boxinfo.add_widget(MDLabel(text=str(video.title), size_hint=(1, 0.3)))
            
            viewsformated = self.converfuncsclass.viewsconv(video.views)
            dateformated = self.converfuncsclass.dateconv(video.publish_date)
            boxviewsage = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.05)) 
            boxviewsage.add_widget(MDLabel(text=f"{viewsformated} de vizualizações",font_size=20, size_hint=(0.5, 1))) #views
            boxviewsage.add_widget(MDLabel(text=f"há {dateformated}", size_hint=(0.5, 1))) #data
            boxinfo.add_widget(boxviewsage)
            
            formated_time = self.converfuncsclass.formtimeseg(video.length)
            boxinfo.add_widget(MDLabel(text=str(video.author), size_hint=(1, 0.3))) #canal
            boxinfo.add_widget(MDLabel(text=str(formated_time), size_hint=(1, 0.3))) #tempo
            boxla.add_widget(boxinfo)
            
            boxla.add_widget(MDRaisedButton(text="Download", size_hint=(0.1, None)))
            boxvideossearch.add_widget(boxla)
            
    pass