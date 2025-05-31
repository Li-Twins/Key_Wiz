from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader

import json
import random
import sys

Builder.load_string('''
<ModeScreen>:
    canvas.before:
        Rectangle:
            source: 'bg2.jpg'
            pos: self.pos
            size: self.size
        Color:
            rgba : 0, 0, 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size
    AnchorLayout:
        anchor_x: 'center'
        anchor_y: 'center'
        BoxLayout:
            orientation: 'vertical'
            padding: [50, 100]
            spacing: 50
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: (0.6, 0.8)
            
            Button:
                text: 'Normal'
                font_size: 40
                valign: 'center'
                halign: 'center'
                size_hint: (1, 0.25)
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.normal_mode()
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.5
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [5]
                    Color:
                        rgba: 0.82, 0.41, 0.12, 1
                    Line:   
                        width: 1
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

            Button:
                text: 'Dev'
                font_size: 40
                size_hint: (1, 0.25)    
                valign: 'center'
                halign: 'center'
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.dev_mode()
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.5
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [5]
                    Color:
                        rgba: 0.82, 0.41, 0.12, 1
                    Line:   
                        width: 1
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

            Button:
                text: 'Quit'
                font_size: 40
                size_hint: (1, 0.25)    
                valign: 'center'
                halign: 'center'
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.quit()
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.5
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [5]
                    Color:
                        rgba: 0.82, 0.41, 0.12, 1
                    Line:   
                        width: 1
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)
''')

class ModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def normal_mode(self):
        pass # placeholder for the actual normal mode

    def dev_mode(self):
        pass # placeholder for the actual dev mode

    def quit(self):
        sys.exit() 

class KeyWizmodeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(ModeScreen(name='mode_screen'))
        return sm

if __name__ == '__main__':
    KeyWizmodeApp().run()