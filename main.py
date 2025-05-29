from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import json
import random

Builder.load_string('''
<DevModeScreen>:
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1  # Dark background
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        Label:
            text: 'Developer Mode'
            font_size: 24  # Smaller title
            bold: True
            size_hint_y: None
            height: 40
            color: 0.9, 0.9, 0.9, 1

        Spinner:
            id: topic_spinner
            text: 'Select Topic'
            size_hint_y: None
            height: 44
            background_color: 0.2, 0.2, 0.2, 1
            color: 1, 1, 1, 1

        Button:
            text: 'Load Questions'
            size_hint_y: None
            height: 50
            background_normal: ''
            background_color: 0.25, 0.25, 0.25, 1
            color: 1, 1, 1, 1
            on_press: root.load_questions()
            canvas.before:
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]

        Label:
            id: question_label
            text: ''
            font_size: 18
            halign: 'left'
            valign: 'top'
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1] + 20
            color: 0.95, 0.95, 0.95, 1

        Label:
            id: answer_label
            text: ''
            font_size: 16
            size_hint_y: None
            height: self.texture_size[1] + 20
            color: 0, 0, 0, 0  # initially invisible

        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 20

            Button:
                text: 'Show Answer'
                background_normal: ''
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_press: root.toggle_answer()
                canvas.before:
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]

            Button:
                text: 'Next'
                background_normal: ''
                background_color: 0.3, 0.3, 0.3, 1
                color: 1, 1, 1, 1
                on_press: root.next_question()
                canvas.before:
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [10]

        Button:
            text: 'Back'
            size_hint_y: None
            height: 50
            background_normal: ''
            background_color: 0.2, 0.2, 0.2, 1
            color: 1, 1, 1, 1
            on_press: app.root.current = 'main'
            canvas.before:
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [10]
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
        if not topic or topic == 'Select Topic':
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
            self.ids.question_label.text = f"Q{self.current_index + 1}: {question}"
            self.ids.answer_label.text = f"Answer: {answer}"
            self.ids.answer_label.color = (0, 0, 0, 0)  # Hide answer
        else:
            self.ids.question_label.text = "No more questions!"
            self.ids.answer_label.text = ""
            self.ids.answer_label.color = (0, 0, 0, 0)

    def toggle_answer(self):
        if self.ids.answer_label.color[3] == 0:
            self.ids.answer_label.color = (1, 1, 1, 1)
        else:
            self.ids.answer_label.color = (0, 0, 0, 0)

    def next_question(self):
        self.current_index += 1
        self.show_question()


class KeyWizApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DevModeScreen(name='dev_mode'))
        return sm

if __name__ == '__main__':
    KeyWizApp().run()