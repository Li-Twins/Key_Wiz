from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

import json
import random
import sys

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
        
        # Top 10% container
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.1  # Takes exactly 10% of screen height
            padding: [10, 0, 10, 0]  # Left/right padding only

            BoxLayout:
                orientation: 'horizontal'
                size_hint_x: 0.8                
            
            # Rolling quote (takes 80% width)
            RollingQuoteLabel:
                id: rolling_quote
                font_size: 40
                font_name: 'zpix.ttf'
                size_hint_x: 1
                valign: 'center'
                halign: 'right'
                color: 0.82, 0.41, 0.12, 1
            
            # Spacer to push button to right
            Widget:
                size_hint_x: 0.1
            
            # Back button container (takes 10% width)
            BoxLayout:
                size_hint_x: 0.1
                padding: [0, 10, dp(30), 10]  # Right padding only
                
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

class MenuScreen(Screen):
    def switch_to_dev_mode(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'dev_mode'         # Change screen

    def switch_to_quiz_mode(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'quiz_mode'         # Change screen

    def quit(self):
        sys.exit()

class QuizScreen(Screen):
    def back_to_root(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'menu'         # Change screen

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
        return sm

if __name__ == '__main__':
    KeyWizApp().run()
