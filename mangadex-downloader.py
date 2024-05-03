from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from converter import Converter
from api import Downloader
from kivy.uix.label import Label
import re
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.config import Config

url_pattern = re.compile(
    r'^(?:http|ftp)s?://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class MangaDownloader(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.inputLabel = Label(text="Enter the link here :",size_hint_y=None, height=40)
        layout.add_widget(self.inputLabel)

        self.url_input = TextInput(hint_text='Enter Mangadex Link', multiline=False,size_hint_y=None, height=40)
        layout.add_widget(self.url_input)
        
        self.checkBox_label = Label(text="Would you like to convert to .webp format?",size_hint_y=None, height=40)
        layout.add_widget(self.checkBox_label)
        
        self.checkBox = CheckBox(height=40)
        layout.add_widget(self.checkBox)
        
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')



        download_button = Button(text='Download',size_hint_y=None, height=50)
        download_button.bind(on_press=self.start_download)
        layout.add_widget(download_button)
        
        return layout

    def start_download(self, instance):
        
        url = self.url_input.text
        if url_pattern.match(url):
            self.checkBox_label.text  = "Started Dont do this"
            downloader = Downloader(url)
            downloader.start()
            if(self.checkBox.active):
                converter = Converter()
                status = converter.start()
                if(status):
                    self.show_alert("Completed", "it has been downloaded and converted it is in the Webps folder")
                    self.checkBox_label.text  = "Would you like to convert to .webp format?"
                else:
                    self.show_alert("Incomplete", "something went wrong please contact tuugii")
            else:
                self.show_alert("Completed", "The chapter's have been downloaded it should be in the ./images folder")
                self.checkBox_label.text  = "Would you like to convert to .webp format?"
        else:
            self.show_alert("Invalid URL", "Please enter a valid URL")

    def show_alert(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        
        popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
            
    def startalert(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="it has started dont do anything please"))
        
        popup = Popup(title="Started", content=content, size_hint=(None, None), size=(400, 200))
        popup.open()
            
if __name__ == '__main__':
    MangaDownloader().run()

