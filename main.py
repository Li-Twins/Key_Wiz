from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, StringProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

import json
import random
import sys
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

#!/sur/bin/python
# -*- coding: utf-8 -*-

QUOTES = [
    "There's more to learn!",
    "Let me teach you the ways of magic!",
    "I got quests!",
    "Magic waits for no one, apprentice!",
    "Still working on that quest?",
    "Shouldn't you be murdering something about now?",
    "Sooooo... how are things?",
    "Hey, best friend!",
    "Away with thee!",
    "Hocus pocus!",
    "Ahhh!",
    "Alaka-ZAM!",
    "Ha-HA!",
    "Commencing directive three! Uhntssuhntssuhntss--",
    "Yes. Remember what? Are... are you my father?",
    "-- Are you god? Am I dead?",
    "I'M DEAD I'M DEAD OHMYGOD I'M DEAD!",
    "Hey everybody! Check out my package!",
    "Let's get this party started!",
    "Recompiling my combat code!",
    "This time it'll be awesome, I promise!",
    "Battlebot go -- Oh that's me",
    "Health! Ooo, what flavor is red?",
    "Health over here!",
    "Sweet life juice!",
    "I found health!",
    "Healsies!",
    "Where'd all my bullets go?",
    "Bullets are dumb.",
    "Who needs ammo anyway, am I right?",
    "I need tiny death pellets!",
    "Need some ammo!",
    "Dangit, I'm out!",
    "Ammo reserves are spent!",
    "Crap, no more shots left!",
    "Hnngh! Empty!",
    "Coming up empty!",
    "Wheeeee!",
    "Yahooooo!",
    "Aaaaaaahhh!",
    "I'm flying! I'm really flying!",
    "Look out below!",
    "Yipe!",
    "Yikes!",
    "Yeehaw!",
    "Hyah!",
    "Heyyah!",
    "Take that!",
    "Bop!",
    "Badass!",
    "Badass?! Aaahhh!",
    "Look out, a Badass!",
    "RUN FOR YOUR LIIIIIVES!!!",
    "Oh, he's big... REALLY big!",
    "Scary Badass dude, over there!",
    "Oh no, Badass!",
    "Save me from the Badass!",
    "Psst! Ad-ass-bay, over ere-bay!",
    "That guy looks an awful lot like a Badass!",
    "Step right up, to the Bulletnator 9000!",
    "I am a tornado of death and bullets!",
    "Stop me before I kill again, except don't!",
    "Hehehehe, mwaa ha ha ha, MWAA HA HA HA!",
    "I'm on a roll!",
    "Unts unts unts unts!",
    "Ha ha ha! Fall before your robot overlord!",
    "Can't touch this!",
    "Ha! Keep 'em coming!",
    "There is no way this ends badly!",
    "This is why I was built!",
    "You call yourself a badass?",
    "Wow, did I really do that?",
    "Is it dead? Can, can I open my eyes now?",
    "I didn't panic! Nope, not me!",
    "Not so tough after all!",
    "One down, any other takers?",
    "I have gaskets tougher than you!",
    "That was me! I did that!",
    "Like running over a bug!",
    "That was a close one!",
    "Don't tell me that wasn't awesome!",
    "Ha ha ha! Suck it!",
    "Wait, did I really do that?",
    "Holy moly!",
    "'Nade out!",
    "Yeah! Single-player bonus!",
    "I must look really stupid right now!",
    "Aww, way to leave me hanging, friend.",
    "Don't you like me?",
    "(Sobbing) I just want to be loved!",
    "I'm a Pandoracorn's butthole!",
    "I fart rainbows!",
    "Bask in my aura of death!",
    "Did you guys see that?!",
    "Ready to go on where you are, friend. Adiamo!",
    "Gosh, this party is worse than stairs."
]

Builder.load_string('''
<QuizScreen>:
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
    
    FloatLayout:
        Button:
            id: back_button
            text: 'O.o'
            on_press: root.back_to_root()
            font_size: 20
            font_name: 'zpix.ttf'
            size_hint: None, None
            size: 50, 50
            pos_hint: {'right': 0.95, 'top': 0.95} # 5% margin from edges
            background_normal: ''
            background_color: 0, 0, 0, 0
            color: 0.82, 0.41, 0.12, 1
            canvas.before:
                # Background
                Color:
                    rgba: 0, 0, 0, 0.5
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [5]
                # Border
                Color:
                    rgba: 0.82, 0.41, 0.12, 1
                Line:
                    width: 1.5
                    rounded_rectangle: (self.x, self.y, self.width, self.height, 5)  
                    
<MenuScreen>:
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
        halign: 'center'
                
        Button:
            text: 'Dev Mode'
            on_press: root.switch_to_dev_mode()
            font_size: 50
            font_name: 'zpix.ttf'
            size_hint: (0.9, 0.3)
            valign: 'top'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 0  # Make transparent
            color: 0.82, 0.41, 0.12, 1
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
            text: 'Quiz Run'
            on_press: root.switch_to_quiz_mode()
            font_size: 50
            font_name: 'zpix.ttf'
            size_hint: (0.9, 0.3)
            valign: 'top'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 0  # Make transparent
            color: 0.82, 0.41, 0.12, 1
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
            text: '2(0.d.0)'
            on_press: root.switch_to_todo_mode()
            font_size: 50
            font_name: 'zpix.ttf'
            size_hint: (0.9, 0.3)
            valign: 'top'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 0  # Make transparent
            color: 0.82, 0.41, 0.12, 1
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
            text: 'Exit >.<'
            on_press: root.quit()
            font_size: 50
            font_name: 'zpix.ttf'
            size_hint: (0.9, 0.3)
            valign: 'top'
            halign: 'center'
            pos_hint: {'center_x': 0.5}
            background_normal: ''
            background_color: 0, 0, 0, 0  # Make transparent
            color: 0.82, 0.41, 0.12, 1
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

                    
<CustomSpinnerOption>:
    background_normal: ''
    background_color: (0, 0, 0, 0.5)
    color: 0.82, 0.41, 0.12, 1
    font_size: 30
    font_name: 'zpix.ttf'
    height: '40dp'
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
                    
<DevModeScreen>:
    canvas.before:
        Rectangle:
            source: 'bg2.jpg'
            pos: self.pos
            size: self.size        
        Color:
            rgba: 0, 0, 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        
        # Top 10pc container
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1  # Takes exactly 10pc of screen height
            padding: [10, 0, 10, 0]  # Left/right padding only

            # Main content area (90% width)
            BoxLayout:
                size_hint_x: 0.9
                orientation: 'horizontal'
                
                # Rolling quote (takes available space)
                RollingQuoteLabel:
                    id: rolling_quote
                    text: "In Key-Wiz We Trust"
                    font_size: 30
                    font_name: 'zpix.ttf'
                    size_hint_x: 1
                    valign: 'center'
                    halign: 'right'
                    color: 0.82, 0.41, 0.12, 1
                    text_size: self.width, None
                    shorten: True
                    shorten_from: 'right'
            
            # Back button container (10% width)
            BoxLayout:
                size_hint_x: 0.1
                padding: [0, 10, 0, 10]  # Removed right padding from here
                
                Button:
                    id: back_button
                    text: 'O.o'
                    on_press: root.back_to_root()
                    font_size: 20
                    font_name: 'zpix.ttf'
                    size_hint: None, None
                    size: 50, 50
                    pos_hint: {'right': 1, 'center_y': 0.5}
                    background_normal: ''
                    background_color: 0, 0, 0, 0
                    color: 0.82, 0.41, 0.12, 1
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
                            width: 1.5
                            rounded_rectangle: (self.x, self.y, self.width, self.height, 5)
                    
        # Rest of your content (takes remaining 90%)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.9
            padding: [20, 20]
            spacing: 20
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}

            Spinner:
                id: topic_spinner
                text: 'Topics'
                font_size: 50
                font_name: 'zpix.ttf'
                size_hint: (0.8, 0.06)
                valign: 'bottom'
                halign: 'center'
                pos_hint: {'center_x': 0.5}
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                option_cls: 'CustomSpinnerOption'
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
                font_size: 50
                font_name: 'zpix.ttf'
                size_hint: (0.8, 0.06)
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
                font_size: 70
                font_name: 'zpix.ttf'
                valign: 'middle'
                halign: 'center'
                text_size: self.width, None
                size_hint: (0.9, 0.3)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                color: 0.91, 0.59, 0.31, 1

            Label:
                id: answer_label
                text: ''
                font_size: 70
                font_name: 'zpix.ttf'
                valign: 'middle'
                halign: 'center'
                text_size: self.width, None
                size_hint: (0.9, 0.3)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                color: 0, 0, 0, 0  # initially invisible

            BoxLayout:
                size_hint: (0.8, 0.08)
                spacing: 20
                padding: [20, 20]
                pos_hint: {'center_x': 0.5}
                spacing: 20

                Button:
                    text: 'Answer'
                    background_normal: ''
                    font_size: 50
                    font_name: 'zpix.ttf'
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
                    font_size: 50
                    font_name: 'zpix.ttf'
                    background_color: 0, 0, 0, 0
                    color: 0.82, 0.41, 0.12, 1
                    on_press: root.next_question()
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

<ToDoScreen>:
    canvas.before:
        Rectangle:
            source: 'bg2.jpg'
            pos: self.pos
            size: self.size        
        Color:
            rgba: 0, 0, 0, 0.5
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        orientation: 'vertical'
        padding: 0
        spacing: 0
        
        # Top 10pc container
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1
            padding: [10, 0, 10, 0]

            # Date label
            Label:
                text: root.current_date
                font_size: 40
                font_name: 'zpix.ttf'
                size_hint_x: 0.9
                valign: 'center'
                halign: 'right'
                color: 0.82, 0.41, 0.12, 1
                text_size: self.width, None
            
            # Back button container
            BoxLayout:
                size_hint_x: 0.1
                padding: [0, 10, 0, 10]
                
                Button:
                    id: back_button
                    text: 'O.o'
                    on_press: root.back_to_root()
                    font_size: 20
                    font_name: 'zpix.ttf'
                    size_hint: None, None
                    size: 50, 50
                    pos_hint: {'right': 1, 'center_y': 0.5}
                    background_normal: ''
                    background_color: 0, 0, 0, 0
                    color: 0.82, 0.41, 0.12, 1
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
                            width: 1.5
                            rounded_rectangle: (self.x, self.y, self.width, self.height, 5)
        
        # Main content area (90%)
        ScrollView:
            id: scroll_view
            size_hint_y: 0.8
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 20
                padding: [20, 20]
                
                # Task buttons
                TaskButton:
                    text: 'Drink Water Lots'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Do Quiz'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Check Belongings'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Sleep at 10pm'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Up by 730am'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Cook Eggs'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'No acting cute'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'No Immature Talk'
                    on_press: root.toggle_task(self)
                TaskButton:
                    text: 'Insight'
                    on_press: root.toggle_task(self)
        
        # Submit button area (10%)
        BoxLayout:
            size_hint_y: 0.1
            padding: [20, 20]
            
            Button:
                text: 'Submit'
                font_size: 50
                font_name: 'zpix.ttf'
                size_hint: (0.8, 1)
                valign: 'middle'
                halign: 'center'
                pos_hint: {'center_x': 0.5}
                background_normal: ''
                background_color: 0, 0, 0, 0
                color: 0.82, 0.41, 0.12, 1
                on_press: root.send_email()
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

<TaskButton@Button>:
    font_size: 40
    font_name: 'zpix.ttf'
    size_hint: (0.8, None)
    height: 80
    pos_hint: {'center_x': 0.5}
    background_normal: ''
    background_color: 0, 0, 0, 0.5
    color: 0.82, 0.41, 0.12, 1
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
                self.ids.topic_spinner.values = sorted([x.title() for x in self.topics]) # display topics as title
        except Exception as e:
            print(f"Error loading topics: {e}")
            self.topics = []
            self.ids.topic_spinner.values = []

    def load_questions(self):
        topic = (self.ids.topic_spinner.text).lower() # change displayed topic into proper lower case for loading
        if not topic or topic == 'Topics':
            return

        try:
            with open(f'kw_{topic}.json', 'r', encoding='utf-8') as f: # ensures chinese encoding             
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

    def back_to_root(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'menu'         # Change screen


class RollingQuoteLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_quote = "In Key-Wiz We Trust"
        self.halign = 'right'
        Clock.schedule_once(self.update_quote, 15)  # Start after 10 second
    
    def update_quote(self, dt):
        # Get a random quote different from the current one
        new_quote = random.choice([q for q in QUOTES if q != self.current_quote])
        self.current_quote = new_quote
        
        # Animation to fade out
        anim_out = Animation(opacity=0, duration=0.5)
        anim_out.bind(on_complete=self._animate_in)
        anim_out.start(self)
    
    def _animate_in(self, animation, widget):
        # Update text when invisible
        widget.text = self.current_quote
        
        # Animation to fade in
        anim_in = Animation(opacity=1, duration=0.5)
        anim_in.start(widget)
        
        # Schedule next quote change
        Clock.schedule_once(self.update_quote, 15)  # Change every 5 seconds
    
class CustomSpinnerOption(SpinnerOption):
    pass # this is required to modify spinner option appearance

class InsightPopup(Popup):
    def __init__(self, todo_screen, **kwargs):
        super().__init__(**kwargs)
        self.todo_screen = todo_screen
        self.title = 'Enter Your Insight'
        self.size_hint = (0.8, 0.4)
        
        # Set popup background to dark theme
        self.background = ''
        self.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
        self.separator_color = (0.82, 0.41, 0.12, 1)  # Orange-brown separator
        self.title_color = (0.82, 0.41, 0.12, 1)  # Orange-brown title
        self.title_size = '30sp'
        self.title_font = 'zpix.ttf'
        
        # Main layout with dark background
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        with layout.canvas.before:
            Color(0, 0, 0, 0.7)  # Dark semi-transparent background
            self.rect = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[5])
        
        # Text input with dark theme
        self.text_input = TextInput(
            multiline=True,
            size_hint_y=0.7,
            font_name='zpix.ttf',
            font_size=30,
            background_color=(0, 0, 0, 0.5),
            foreground_color=(0.82, 0.41, 0.12, 1),
            cursor_color=(0.82, 0.41, 0.12, 1),
            selection_color=(0.82, 0.41, 0.12, 0.5)
        )
        
        # Button layout
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        # Submit button
        submit_btn = Button(
            text='Submit',
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.82, 0.41, 0.12, 1)
        )
        
        # Cancel button
        cancel_btn = Button(
            text='Cancel',
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.82, 0.41, 0.12, 1)
        )
        
        # Add buttons to layout
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(submit_btn)
        Clock.schedule_once(lambda dt: self.style_buttons(submit_btn, cancel_btn))
        
        # Add widgets to main layout
        layout.add_widget(self.text_input)
        layout.add_widget(btn_layout)
        self.content = layout

        submit_btn.bind(on_press=self.submit_insight)
        cancel_btn.bind(on_press=self.dismiss)
        
        # Update layout when size changes
        layout.bind(pos=self.update_rect, size=self.update_rect)
    
    # next two functions fix the mysterious square
    def style_buttons(self, *buttons):
        for btn in buttons:
            with btn.canvas.before:
                # Border
                Color(0.82, 0.41, 0.12, 1)
                RoundedRectangle(pos=btn.pos, size=btn.size, radius=[5])
                # Inner fill
                Color(0, 0, 0, 0.5)
                RoundedRectangle(
                    pos=(btn.x+1, btn.y+1),
                    size=(btn.width-2, btn.height-2),
                    radius=[5]
                )
            btn.bind(pos=self.update_button_style, size=self.update_button_style)

    def update_button_style(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Border
            Color(0.82, 0.41, 0.12, 1)
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[5])
            # Inner fill
            Color(0, 0, 0, 0.5)
            RoundedRectangle(
                pos=(instance.x+1, instance.y+1),
                size=(instance.width-2, instance.height-2),
                radius=[5]
            )
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def submit_insight(self, instance):
        insight_text = self.text_input.text.strip()
        if insight_text:
            self.todo_screen.insight_text = insight_text
            # Get the ScrollView's child (the BoxLayout containing buttons)
            scroll_view = self.todo_screen.ids['scroll_view']  # Proper dictionary access
            button_container = scroll_view.children[0]  # The BoxLayout inside ScrollView
            
            # Find and update the Insight button
            for child in button_container.children:
                if isinstance(child, Button) and child.text == 'Insight':
                    child.background_color = (0.5, 0.5, 0.5, 0.5)
                    child.color = (0.7, 0.7, 0.7, 1)
                    if 'Insight' not in self.todo_screen.completed_tasks:
                        self.todo_screen.completed_tasks.append('Insight')
                    break
        self.dismiss()

class MenuScreen(Screen):
    def switch_to_dev_mode(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'dev_mode'         # Change screen

    def switch_to_quiz_mode(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'quiz_mode'         # Change screen

    def switch_to_todo_mode(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'todo'

    def quit(self):
        sys.exit()

class QuizScreen(Screen):
    def back_to_root(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'menu'         # Change screen

class ToDoScreen(Screen):
    current_date = StringProperty() # fix for traceback when calling current_date in builder
    insight_text = StringProperty("")  # To store the insight text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.completed_tasks = []
        self.insight_text = ""
    
    def toggle_task(self, button):
        if button.text == 'Insight':
            InsightPopup(todo_screen=self).open()
        else:
            if button.text in self.completed_tasks:
                self.completed_tasks.remove(button.text)
                button.background_color = (0, 0, 0, 0.5)
                button.color = (0.82, 0.41, 0.12, 1)
            else:
                self.completed_tasks.append(button.text)
                button.background_color = (0.5, 0.5, 0.5, 0.5)
                button.color = (0.7, 0.7, 0.7, 1)
    
    def send_email(self):
        try:
            # Email configuration
            sender = "ellisereli@gmail.com"  # Replace with your email
            password = "apbq essb gler slhq"       # Replace with your password
            recipient = "ellisereli@gmail.com"
            
            # Create message
            subject = f"ToDo List Update - {self.current_date}"
            body = f"Completed tasks on {self.current_date}:\n\n"
            body += "\n".join(self.completed_tasks) if self.completed_tasks else "No tasks completed today"

            if self.insight_text:
                body += "\n\nInsight:\n" + self.insight_text
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            
            # Send email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender, password)
                smtp.send_message(msg)
            
            # Show confirmation
            self.show_popup("Success", "Email sent successfully!")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to send email: {str(e)}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text=message,
            font_name='zpix.ttf',
            font_size=30,
            color=(0.82, 0.41, 0.12, 1)
        ))
        
        btn = Button(
            text='OK',
            size_hint=(1, 0.3),
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.82, 0.41, 0.12, 1)
        )
        
        popup = Popup(
            title=title,
            title_font='zpix.ttf',
            title_size='30sp',
            title_color=[0.82, 0.41, 0.12, 1],
            content=content,
            size_hint=(0.7, 0.4),
            separator_color=[0.82, 0.41, 0.12, 1],
            background='',
            background_color=(0, 0, 0, 0.8) # 0.8 transparency of pop up, 0 is transparent
        )
        
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        
        popup.open()
    
    def back_to_root(self): # exit to root button action
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'menu'

class KeyWizApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.05, 1) 
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: Window.canvas.ask_update(), 0.1) # fix for black screen at start up
        self.sound = SoundLoader.load('music.mp3')     
        if self.sound:
            self.sound.loop = True  # Enable looping
            self.sound.play()
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(DevModeScreen(name='dev_mode'))
        sm.add_widget(QuizScreen(name='quiz_mode'))
        sm.add_widget(ToDoScreen(name='todo'))
        return sm

if __name__ == '__main__':
    KeyWizApp().run()