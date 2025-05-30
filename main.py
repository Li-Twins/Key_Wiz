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


Builder.load_string('''
<DevModeScreen>:
    canvas.before:
        Rectangle:
            source: 'bg2.jpg'
            pos: self.pos
            size: self.size        
        Color:
            rgba: 0, 0, 0, 0.5 # Dark background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: [20, 20]
        spacing: 20
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        halign: 'center'

        Label:
            text: 'Key Wiz Dev Mode'
            font_size: 40  # Smaller title
            bold: True
            size_hint: (1, 0.1)
            pos_hint: {'center_x': 0.5}
            valign: 'top'
            halign: 'center'
            color: 0.82, 0.41, 0.12, 1

        Spinner:
            id: topic_spinner
            text: 'Topics'
            font_size: 40
            size_hint: (0.7, 0.1)
            valign: 'bottom'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_color: 0, 0, 0, 0
            color: 0.82, 0.41, 0.12, 1
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 0.5 # Button fill color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]
                Color:
                    rgba: 0.82, 0.41, 0.12, 1  # Border color
                Line:
                    width: 1
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

        Button:
            text: 'Load Questions'
            font_size: 40
            size_hint: (0.7, 0.1)
            valign: 'top'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 0  # Make transparent
            color: 0.82, 0.41, 0.12, 1
            on_press: root.load_questions()
            canvas.before:
                Color:
                    rgba: 0, 0, 0, 0.5  # Button fill color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]
                Color:
                    rgba: 0.82, 0.41, 0.12, 1 # Border color
                Line:
                    width: 1
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

        Label:
            id: question_label
            text: ''
            font_size: 50
            valign: 'middle'
            halign: 'center'
            text_size: self.width, None
            size_hint: (0.8, 0.2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            color: 0.91, 0.59, 0.31, 1

        Label:
            id: answer_label
            text: ''
            font_size: 50
            valign: 'middle'
            halign: 'center'
            text_size: self.width, None
            size_hint: (0.8, 0.2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            color: 0, 0, 0, 0  # initially invisible

        BoxLayout:
            size_hint: (0.7, 0.15)
            spacing: 20
            padding: [20, 20]
            pos_hint: {'center_x': 0.5}
            spacing: 20

            Button:
                text: 'Show Answer'
                background_normal: ''
                font_size: 40
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.toggle_answer()
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.5  # Button fill color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [5]
                    Color:
                        rgba: 0.82, 0.41, 0.12, 1 # Border color
                    Line:
                        width: 1
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

            Button:
                text: 'Next'
                background_normal: ''
                font_size: 40
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.next_question()
                canvas.before:
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.5  # Button fill color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [5]
                    Color:
                        rgba: 0.82, 0.41, 0.12, 1  # Border color
                    Line:
                        width: 1
                        rounded_rectangle: (self.x, self.y, self.width, self.height, 5)

''')


class DevModeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = []
        self.current_index = 0
        self.topics = []
        self.load_topics()

    def on_pre_enter(self, *args):
        self.load_topics()

    def load_topics(self):
        try:
            with open('kw_topics.json', 'r') as f:
                self.topics = json.load(f)
                self.ids.topic_spinner.values = self.topics
                if self.topics:
                    self.ids.topic_spinner.text = self.topics[0]
        except Exception as e:
            print(f"Error loading topics: {e}")
            self.topics = []
            self.ids.topic_spinner.values = []

    def load_questions(self):
        topic = self.ids.topic_spinner.text
        if not topic or topic == 'Topics':
            return

        try:
            with open(f'kw_{topic}.json', 'r') as f:
                self.questions = json.load(f)
                random.shuffle(self.questions)
                self.current_index = 0
                self.show_question()
        except Exception as e:
            print(f"Error loading questions: {e}")

    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = f"{question}"
            self.ids.answer_label.text = f"{answer}"
            self.ids.answer_label.color = (0, 0, 0, 0)  # Hide answer
        else:
            self.ids.question_label.text = "No more questions!"
            self.ids.answer_label.text = ""
            self.ids.answer_label.color = (0, 0, 0, 0)

    def toggle_answer(self):
        if self.ids.answer_label.color[3] == 0:
            self.ids.answer_label.color = (0.91, 0.59, 0.31, 1)
        else:
            self.ids.answer_label.color = (0, 0, 0, 0)

    def next_question(self):
        self.current_index += 1
        self.show_question()


class KeyWizApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1) 
        self.sound = SoundLoader.load('music.mp3')     
        if self.sound:
            self.sound.loop = True  # Enable looping
            self.sound.play()
        sm = ScreenManager()
        sm.add_widget(DevModeScreen(name='dev_mode'))
        return sm

if __name__ == '__main__':
    KeyWizApp().run()
