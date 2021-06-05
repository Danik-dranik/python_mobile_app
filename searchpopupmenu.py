from kivymd.uix.dialog import MDInputDialog
from urllib import parse
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
import certifi
from kivy.clock import Clock
import requests
from kivy.properties import ObjectProperty



class SearchPopupMenu(MDInputDialog):
    maps = ObjectProperty(None)
    title = 'Поиск по адресу'
    text_button_ok = 'Поиск'

    def __init__(self):
        super().__init__()
        self.size_hint = [.9, .3]
        self.events_callback = self.callback

    def open(self):
        super().open()
        Clock.schedule_once(self.set_field_focus, 0.5)

    def callback(self, *args):
        URL = "https://geocode.search.hereapi.com/v1/geocode"
        address = self.text_field.text
        print(address)
        location = address
        api_key = '2Nmhize-Lxxc_DAePAaYLbhmlkRy7l_Lh7MmcuQnV4s' 
        PARAMS = {'apikey':api_key,'q':location} 
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json()
        latitude = data['items'][0]['position']['lat']
        longitude = data['items'][0]['position']['lng']
        print(latitude,longitude)

        #mapview = App.ToolScreenFile
        #mapview.center_on(lat, lon)




