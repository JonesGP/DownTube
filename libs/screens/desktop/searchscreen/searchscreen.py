from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from pytube import Search
class SearchScreen(MDScreen):
    pass
    
class MySearchFunctions:
    def searchvideos(self, text, boxvideossearch):
        sea = Search(text)
        for video in sea.results:
            print(video.title)
            boxla = MDBoxLayout(orientation='horizontal', size_hint_y=None, size_hint_x=1, height=100, padding=5)
            boxla.add_widget(AsyncImage(source=video.thumbnail_url, size_hint=(0.3, 1)))
            
            boxinfo = MDBoxLayout(orientation='vertical', size_hint=(0.7, 1))
            boxinfo.add_widget(MDLabel(text=str(video.title), size_hint=(1, 0.3)))
            
            boxviewsage = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.05))	
            boxviewsage.add_widget(MDLabel(text=f"{str(video.views)} de vizualizações",font_size=20, size_hint=(0.5, 1)))
            boxviewsage.add_widget(MDLabel(text=f"há {str(video.publish_date)}", size_hint=(0.5, 1)))
            boxinfo.add_widget(boxviewsage)
            
            boxinfo.add_widget(MDLabel(text=str(video.author), size_hint=(1, 0.3)))
            boxinfo.add_widget(MDLabel(text=str(video.length), size_hint=(1, 0.3)))
            boxla.add_widget(boxinfo)
            
            boxla.add_widget(MDRaisedButton(text="Download", size_hint=(0.1, None)))
            boxvideossearch.add_widget(boxla)
            
    pass