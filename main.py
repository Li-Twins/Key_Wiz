from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, RoundedRectangle, Rectangle

import re
import json
import random
import sys
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path

global current_player_data, full_player_data, current_player_name 
global APP
APP = None
current_player_data = {
        "removed": [],
        "removed_topics": [],
        "points": 0,
        "latest_code": 0,
        "color": "dark", 
        "background": "bg2.jpg",
        "music": "music.mp3",
        "font": "zpix.ttf",
        "quotes": "clap"
}

# Android-specific imports with fallback
try:
    from android.storage import app_storage_path
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.READ_EXTERNAL_STORAGE, 
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.INTERNET
    ])
    ANDROID = True
except ImportError:
    ANDROID = False

# Storage handling functions
def get_app_storage():
    """Returns the correct storage path, checking both possible locations"""
    if ANDROID:
        from android.storage import app_storage_path
        base_path = app_storage_path()  # /data/user/0/org.test.kwdev/files/
        app_path = os.path.join(base_path, 'app')  # /data/user/0/org.test.kwdev/files/app/
        
        # Check if our files are in the app/ subdirectory
        if os.path.exists(os.path.join(app_path, 'kw_gui_players.json')):
            return app_path
        return base_path
    else:
        return os.path.abspath(".")

def get_data_path():
    """Gets path to data directory, creates if needed"""
    base_path = get_app_storage()
    data_path = os.path.join(base_path, 'data')
    os.makedirs(data_path, exist_ok=True)
    return data_path

def get_quote_path():
    """Gets path to quote files"""
    data_path = get_data_path()
    quote_path = os.path.join(data_path, 'quote')
    os.makedirs(quote_path, exist_ok=True)
    return quote_path

def get_json_path(filename):
    """Gets path for JSON files with Android path workaround"""
    storage = get_app_storage()
    # First check in app/ subdirectory
    app_path = os.path.join(storage, 'app', filename)
    if os.path.exists(app_path):
        return app_path
    # Fall back to regular path
    return os.path.join(storage, filename)

def load_quote_file(filename):
    """Loads quote files with fallback"""
    quote_path = get_quote_path()
    filepath = os.path.join(quote_path, filename)
    
    if not os.path.exists(filepath):
        # Provide default content if file doesn't exist
        default_content = ["Where is everybody?"]
        with open(filepath, 'w') as f:
            f.writelines(default_content)
    
    with open(filepath, 'r') as f:
        return f.readlines()

# Load quote files with error handling
try:
    CLAP = load_quote_file('clap.txt')
    SLAP = load_quote_file('slap.txt')
    FLAP = load_quote_file('flap.txt')
    QUOTES = CLAP[:]
except Exception as e:
    print(f"Error loading quotes: {e}")
    CLAP = SLAP = FLAP = QUOTES = ["Woot! It DOESNT WORK!"]

# Load player data with error handling
try:
    player_file = get_json_path('kw_gui_players.json')
    full_player_data = json.load(open(player_file, 'r'))
except Exception as e:
    print(f"Error loading player data: {e}")
    full_player_data = {}
    # current_player_data already has default values


class BaseScreen(Screen):
    current_date = StringProperty() 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_pre_enter=self.update_style)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        with self.canvas.before:
            self.bg_image = Rectangle(source='', pos=self.pos, size=self.size)
            Color(0, 0, 0, 0.5)
            self.bg_overlay = Rectangle(pos=self.pos, size=self.size)
    
    def update_child_colors(self, widget=None):
        """Recursively update colors for all widgets"""
        widget = widget or self
        app = App.get_running_app()
        
        if hasattr(widget, 'color'):
            widget.color = app.color_scheme
        if hasattr(widget, 'font_name'):
            widget.font_name = app.current_font
            
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.update_child_colors(child)
    
    def _update_rect(self, instance, value):
        """Update rectangle positions/sizes when screen changes"""
        self.bg_image.pos = self.pos
        self.bg_image.size = self.size
        self.bg_overlay.pos = self.pos
        self.bg_overlay.size = self.size
    
    def update_style(self, *args):
        """Update visual elements when screen becomes active"""
        app = App.get_running_app()
        self.bg_image.source = app.current_bg_image

class SettingsScreen(BaseScreen):
    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'
    
class LoginScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def go_to_menu(self, *args):
        """Transition to menu screen"""
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'menu'

    def login(self):
        global full_player_data, current_player_data, current_player_name
        nameinput = self.ids.username_input.text.strip()
        pwinput = self.ids.password_input.text.strip()
            
        if nameinput in full_player_data.keys():
            if pwinput.strip().lower() != full_player_data[nameinput]["passcode"]:
                self.ids.status_label.text = "Password invalid"
                return
                
            # Login successful
            current_player_name = nameinput[:]
            current_player_data = full_player_data[current_player_name]
            APP.load_player_settings()
            self.ids.username_input.text = f"{current_player_name}"
            self.ids.password_input.text = f"Pts: {current_player_data['points']}"
            self.ids.login_button.text = '[ Welcome ]'
        else:    
            self.ids.status_label.text = 'Username not valid.'
            return
        
    def handle_login_button(self):
        if self.ids.login_button.text == '[ Lo.Gin ]':
            self.login()
        else:
            self.go_to_menu()

    def show_message(self, message):
        """Show status message with animation"""
        self.ids.status_label.text = message
        self.ids.status_label.color = APP.color_scheme
        Animation(opacity=1, duration=0.3).start(self.ids.status_label)
        Clock.schedule_once(lambda dt: Animation(opacity=0, duration=2).start(self.ids.status_label), 3)

class NoteItem(BoxLayout):
    note_text = StringProperty('')
    notes_screen = ObjectProperty(None)
    
    def delete_note(self):
        if self.notes_screen:
            self.notes_screen.delete_note(self.note_text)

class NotesScreen(BaseScreen):
    notes = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(notes=self.update_note_display)
        self.notes_file = get_json_path('notes.txt')
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        #self.load_notes()
    
    def delete_note(self, note_text):
        # Remove the note from the list
        self.notes = [note for note in self.notes if note != note_text]
        
        # Save the updated list
        try:
            with open(self.notes_file, 'w') as f:
                f.write('\n'.join(self.notes))
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def update_note_display(self, instance, notes):
        notes_container = self.ids.notes_container
        notes_container.clear_widgets()
        notes_container.spacing = 30
        
        for note in reversed(notes):
            note_item = NoteItem()
            note_item.ids.note_text.text = note
            note_item.note_text = note
            note_item.notes_screen = self
            notes_container.add_widget(note_item)
                            
    def on_pre_enter(self, *args):
        self.load_notes()
        
    def load_notes(self):
        try:
            with open(self.notes_file, 'r') as f:
                content = f.read()
                
                # Split by lines starting with date pattern "YYYY-MM-DD"
                notes = re.split(r'(?m)^(\d{4}-\d{2}-\d{2}:)', content) # list with date followed by content
                for i in range(1, len(notes), 2): # merge the notes back, two items at a time
                    note = notes[i] + notes[i+1]
                    self.notes.append(note.strip())                    
        except Exception as e:
            pass
                
    def save_note(self):
        note_text = self.ids.note_input.text.strip()
        if note_text:
            try:
                note_text = f"{self.current_date}: {note_text}"
                with open(self.notes_file, 'a') as f:
                    f.write(note_text + '\n')
                self.ids.note_input.text = ''
                self.notes.append(note_text)  # Update the notes property
            except Exception as e:
                pass
                
    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(
            text=message,
            font_name='zpix.ttf',
            font_size=20,
            color=self.app.color_scheme
        ))
        
        btn = Button(
            text='OK',
            size_hint=(1, 0.3),
            font_name='zpix.ttf',
            font_size=20,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=self.app.color_scheme
        )
        
        popup = Popup(
            title='Error',
            title_font='zpix.ttf',
            title_size='20sp',
            title_color=[0.88, 0.47, 0.18, 1],
            content=content,
            size_hint=(0.7, 0.4),
            separator_color=[0.88, 0.47, 0.18, 1],
            background='',
            background_color=(0, 0, 0, 0.8)
        )
        
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()
                
    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'
        self.notes=[] # reset notes so no duplicates

class DevModeScreen(BaseScreen):
    show_answer = BooleanProperty(False)
    edit_mode = BooleanProperty(False)  # New property to track edit mode

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(show_answer=self.update_answer_visibility)
        App.get_running_app().bind(
            color_scheme=self.update_answer_style,
            current_font=self.update_answer_style
        )         # Bind to app properties
        self.questions = []
        self.current_index = 0
        self.topics = []
        self.load_topics()

    def switch_to_edit_mode(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'edit_topic'

    def update_answer_visibility(self, instance, value):
        """Toggle answer visibility"""
        if value and self.current_index < len(self.questions):
            self.ids.answer_label.opacity = 1
        else:
            self.ids.answer_label.opacity = 0
    
    def update_answer_style(self, *args):
        """Update answer label style dynamically"""
        app = App.get_running_app()
        answer_label = self.ids.answer_label
        answer_label.color = app.color_scheme
        answer_label.font_name = app.current_font
        
        # Force texture update
        answer_label.texture_update()

    def on_pre_enter(self, *args):
        self.load_topics()

    def load_topics(self):
        try:
            topics_file = get_json_path('kw_topics.json')
            with open(topics_file, 'r') as f:
                self.topics = json.load(f)
                self.ids.topic_spinner.values = sorted([x.title() for x in self.topics]) # display topics as title
        except Exception as e:
            print(f"Error loading topics: {e}")
            self.topics = []
            self.ids.topic_spinner.values = []

    def load_questions(self):
        try:
            topic = self.ids.topic_spinner.text.lower()
            if not topic or topic == 'topics':
                return
                
            topic_file = get_json_path(f'kw_{topic}.json')
            if not os.path.exists(topic_file):
                raise FileNotFoundError(f"kw_{topic}.json not found")
                
            with open(topic_file, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
                random.shuffle(self.questions)
                self.current_index = 0
                self.show_question()
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.show_error_popup(f"Failed to load questions: {e}")
                
        except:
            pass

    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = question
            self.ids.answer_label.text = answer
            self.show_answer = False  # Reset visibility
        else:
            self.ids.question_label.text = "No more questions!"
            self.ids.answer_label.text = ""
            self.ids.answer_label.color = (0, 0, 0, 0)

    def toggle_answer(self):
        if self.ids.answer_label.opacity == 0:
            self.ids.answer_label.opacity = 1
        else:
            self.ids.answer_label.opacity = 0

    def next_question(self):
        self.current_index += 1
        self.ids.answer_label.opacity = 0
        self.show_question()

    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='right')       # Set transition direction
        sm.current = 'menu'         # Change screen

class EditTopicScreen(BaseScreen):
    current_topic = StringProperty('')
    topic_exists = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.topic_file = ''
        self.current_topic = ''
        self.topic_exists = ''

    def delete_topic(self):
        topic_name = self.ids.topic_input.text.strip().lower()
        topic_exist = os.path.exists(f'kw_{topic_name}.json')
        if topic_name != '' and topic_exist == True:
            os.remove(f'kw_{topic_name}.json')
            self.ids.topic_input.text = ''
            self.ids.status_label.text = f'{topic_name.title()} deleted.'
        else:
            self.ids.status_label.text = "Topic doesn't exist yet."
            
    def check_topic(self):
        topic_name = self.ids.topic_input.text.strip().lower()
        if not topic_name: 
            self.ids.status_label.text = "enter topic name"
            return
            
        self.current_topic = topic_name
        self.topic_file = get_json_path(f'kw_{self.current_topic}.json')
        self.topic_exists = os.path.exists(self.topic_file)
        
        if self.topic_exists:
            try:
                with open(self.topic_file, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
                self.ids.status_label.text = f"'{self.current_topic}' ({len(questions)})"
            except Exception as e:
                self.ids.status_label.text = f"Error loading topic: {str(e)}"
        else:
            self.ids.status_label.text = f"New topic: '{self.current_topic}'"
    
    def add_question(self):
        if not self.current_topic:
            self.ids.status_label.text = "Please input a topic first"
            return
            
        question = self.ids.question_input.text.strip()
        answer = self.ids.answer_input.text.strip()
        
        if not question or not answer:
            self.ids.status_label.text = "Need both question and answer!"
            return
            
        try:
            questions = []
            if os.path.exists(self.topic_file):
                with open(self.topic_file, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
            
            questions.append([question, answer])
            
            with open(self.topic_file, 'w', encoding='utf-8') as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
                
            if not self.topic_exists:
                dev_screen = self.manager.get_screen('dev_mode')
                if self.current_topic not in dev_screen.topics:
                    dev_screen.topics.append(self.current_topic)
                    dev_screen.ids.topic_spinner.values = sorted([x.title() for x in dev_screen.topics])
                    topics_file = get_json_path('kw_topics.json')
                    with open(topics_file, 'w') as f:
                        json.dump(dev_screen.topics, f)
                self.topic_exists = True
                
            self.ids.status_label.text = f"Added to '{self.current_topic}' ({len(questions)})"
            self.ids.question_input.text = ''
            self.ids.answer_input.text = ''
        except Exception as e:
            self.ids.status_label.text = f"Error: {str(e)}"
    
    def back_to_dev_mode(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'         
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'dev_mode'

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
        self.app = App.get_running_app()
        self.title = 'Enter Your Insight'
        self.size_hint = (0.8, 0.4)
        
        # Set popup background to dark theme
        self.background = ''
        self.background_color = (0.1, 0.1, 0.1, 1)  # Dark background
        self.separator_color = self.app.color_scheme  # Orange-brown separator
        self.title_color = self.app.color_scheme  # Orange-brown title
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
            foreground_color=self.app.color_scheme,
            cursor_color=self.app.color_scheme,
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
            color=self.app.color_scheme
        )
        
        # Cancel button
        cancel_btn = Button(
            text='Cancel',
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=self.app.color_scheme
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
                Color(self.app.color_scheme)
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
            Color(self.app.color_scheme)
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

class MenuScreen(BaseScreen):

    app = ObjectProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.reinit()   # triggered everytime the screen is accessed, animation change   
    
    def reinit(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'        

    def on_pre_enter(self, *args): # reload with reinit()
        self.reinit()   

    def switch_to_dev_mode(self):
        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='left')       # Set transition direction
        sm.current = 'dev_mode'         # Change screen

    def switch_to_todo_mode(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'todo'

    def switch_to_notes_mode(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'notes'

    def switch_to_sauce_mode(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'sauce'

    def switch_to_settings(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'settings'

    def switch_to_quiz_mode(self):
        # Create the content for the popup
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        
        # Add title label
        title_label = Label(
            text='- SELECT QUIZ MODE -',
            font_size=40,
            font_name= self.app.current_font,
            color= self.app.color_scheme,
            size_hint_y=0.2
        )
        content.add_widget(title_label)
        
        # Create buttons for each mode
        modes = [
            ('Single Minded', 'quiz_single'),
            ('Golden Mean', 'quiz_normal'),
            ("Pandora's Box", 'quiz_all')
        ]
        
        for mode_text, mode_id in modes:
            btn = Button(
                text=mode_text,
                font_size=60,
                font_name= self.app.current_font,
                size_hint_y=0.2,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color= self.app.color_scheme
            )
            btn.bind(on_press=lambda instance, mode=mode_id: self.select_quiz_mode(mode))
            content.add_widget(btn)
        
        # Create the popup
        self.quiz_mode_popup = Popup(
            title='',
            content=content,
            size_hint=(0.8, 0.6),
            separator_height=0,
            background='',
            background_color=(0, 0, 0, 0.5),
            title_color=[0.88, 0.47, 0.18, 1],
            separator_color=[0.88, 0.47, 0.18, 1],
        )
        
        # Style the popup buttons 
        self.quiz_mode_popup.open()

    def select_quiz_mode(self, mode):
        # Close the popup
        self.quiz_mode_popup.dismiss()
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = mode

    def switch_to_study_mode(self):
        sm = self.manager
        sm.transition = SlideTransition(direction='left')
        sm.current = 'study'

    def quit(self):
        global current_player_data, full_player_data, current_player_name
        full_player_data[current_player_name] = current_player_data
        json.dump(full_player_data, open(get_json_path('kw_gui_players.json'), 'w'))
        sys.exit()

class ToDoScreen(BaseScreen):
    insight_text = StringProperty("")  # To store the insight text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
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
                button.color = (0.88, 0.47, 0.18, 1)
            else:
                self.completed_tasks.append(button.text)
                button.background_color = (0.5, 0.5, 0.5, 0.5)
                button.color = (0.7, 0.7, 0.7, 1)
    
    def send_email(self):
        try:
            # Configuration - consider moving these to a config file
            sender = "ellisereli@gmail.com"
            password = "apbq essb gler slhq"  # App password recommended
            recipient = "ellisereli@gmail.com"
            
            # Create message
            subject = f"{current_player_name} - ToDo List - {self.current_date}"
            body = f"Completed tasks on {self.current_date}:\n\n"
            body += "\n".join(self.completed_tasks) if self.completed_tasks else "No tasks completed today"
            
            if self.insight_text:
                body += "\n\nInsight:\n" + self.insight_text
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
                    
            # Send email
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(sender, password)
                smtp.send_message(msg)
                    
            
        except Exception as e:
            pass

        self.back_to_root()
    
    def back_to_root(self): # exit to root button action
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'

class QuizSingleScreen(BaseScreen):
    show_answer = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(show_answer=self.update_answer_visibility)
        App.get_running_app().bind(
            color_scheme=self.update_answer_style,
            current_font=self.update_answer_style
        )         # Bind to app properties
        self.questions = []
        self.current_index = 0
        self.topics = []
        self.removed = []
        self.correct_questions = 0
        self.load_topics()

    def update_answer_visibility(self, instance, value):
        """Toggle answer visibility"""
        if value and self.current_index < len(self.questions):
            self.ids.answer_label.opacity = 1
        else:
            self.ids.answer_label.opacity = 0
    
    def update_answer_style(self, *args):
        """Update answer label style dynamically"""
        app = App.get_running_app()
        answer_label = self.ids.answer_label
        answer_label.color = app.color_scheme
        answer_label.font_name = app.current_font
        # Force texture update
        answer_label.texture_update()

    def on_pre_enter(self, *args):
        self.load_topics()

    def load_topics(self):
        try:
            topics_file = get_json_path('kw_topics.json')
            with open(topics_file, 'r') as f:
                self.topics = json.load(f)
                self.ids.topic_spinner.values = sorted([x.title() for x in self.topics])
        except Exception as e:
            print(f"Error loading topics: {e}")
            self.topics = []
            self.ids.topic_spinner.values = []
            self.show_error_popup(f"Failed to load topics: {e}")

    def load_questions(self):
        try:
            topic = self.ids.topic_spinner.text.lower()
            if not topic or topic == 'topics':
                return
                
            topic_file = get_json_path(f'kw_{topic}.json')
            if not os.path.exists(topic_file):
                raise FileNotFoundError(f"kw_{topic}.json not found")
                
            with open(topic_file, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
                random.shuffle(self.questions)
                self.questions = [q for q in self.questions if q not in self.removed]
                self.current_index = 0
                self.show_question()
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.show_error_popup(f"Failed to load questions: {e}")

    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = question
            self.ids.answer_label.text = answer
        elif self.current_index >= len(self.questions) and [q for q in self.questions if q not in self.removed]:
            self.load_questions()
        else:
            self.ids.question_label.text = f"Score: {self.correct_questions}"
            self.ids.answer_label.text = ""
            self.on_pre_enter()

    def toggle_answer(self):
        if self.ids.question_label.text != f'Score: {self.correct_questions}':
            if self.ids.answer_label.opacity == 0:
                self.ids.answer_label.opacity = 1
            else:
                self.ids.answer_label.opacity = 0

    def next_question(self):
        self.current_index += 1
        self.ids.answer_label.opacity = 0
        self.ids.correct_button.text = 'Correct'
        self.ids.answer_input.text = ''
        self.ids.answer_input.hint_text = f'Score: {self.correct_questions}'
        self.show_question()

    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        sm = self.manager
        sm.transition = SlideTransition(direction='right')
        sm.current = 'menu'

    def mark_correct(self):
        if self.ids.question_label.text != f'Score: {self.correct_questions}':
            if self.ids.correct_button.text == 'Correct':
                self.correct_questions += 1
                self.removed.append(self.questions[self.current_index])
                self.ids.correct_button.text = str(self.correct_questions)

            else:
                self.correct_questions -= 1
                if self.questions[self.current_index] in self.removed:
                    self.removed.remove(self.questions[self.current_index])
                self.ids.correct_button.text = 'Correct'

class QuizAllScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        App.get_running_app().bind(
            color_scheme=self.update_answer_style,
            current_font=self.update_answer_style
        )         # Bind to app properties
        global player_data
        self.questions = []
        self.current_index = 0
        self.topics = []
        self.correct_questions = 0
        self.removed = []
        self.load_topics()

    
    def update_answer_style(self, *args):
        """Update answer label style dynamically"""
        app = App.get_running_app()
        answer_label = self.ids.answer_label
        answer_label.color = app.color_scheme
        answer_label.font_name = app.current_font
        
        # Force texture update
        answer_label.texture_update()

    def on_pre_enter(self, *args):
        self.load_topics()

    def load_topics(self):
        try:
            topics_file = get_json_path('kw_topics.json')
            with open(topics_file, 'r') as f:
                self.topics = json.load(f)
                self.ids.topic_label.text = random.choice(self.topics)
        except Exception as e:
            print(f"Error loading topics: {e}")
            self.topics = []
            self.ids.topic_label.text = "No topics available"
            self.show_error_popup(f"Failed to load topics: {e}")

    def load_questions(self):
        try:
            topic = self.ids.topic_label.text.lower()
            if not topic or topic == 'topics':
                return
                
            topic_file = get_json_path(f'kw_{topic}.json')
            if not os.path.exists(topic_file):
                raise FileNotFoundError(f"kw_{topic}.json not found")
                
            with open(topic_file, 'r', encoding='utf-8') as f:
                self.all_questions = json.load(f)
                self.questions = [x for x in self.all_questions if x not in self.removed]
                if self.questions:
                    self.questions = random.choices(self.all_questions, k=10)
                    self.current_index = 0
                    self.show_question()
        except Exception as e:
            print(f"Error loading questions: {e}")
            self.show_error_popup(f"Failed to load questions: {e}")

    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = question
            self.ids.answer_label.text = answer
        else:
            self.ids.question_label.text = f"Score: {self.correct_questions}"
            self.ids.answer_label.text = ""
            self.on_pre_enter()

    def toggle_answer(self):
        if self.ids.answer_label.opacity == 0:
            self.ids.answer_label.opacity = 1
        else:
            self.ids.answer_label.opacity = 0

    def next_question(self):
        self.current_index += 1
        self.ids.answer_label.opacity = 0
        self.ids.correct_button.text = 'Correct'
        self.ids.answer_input.text = ''
        self.ids.answer_input.hint_text = f'Score: {self.correct_questions}'
        self.show_question()

    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        sm = self.manager
        sm.transition = SlideTransition(direction='right')
        sm.current = 'menu'

    def mark_correct(self):
        question = str(self.ids.question_label.text)
        if self.ids.correct_button.text == 'Correct':
            self.correct_questions += 1
            self.ids.correct_button.text = str(self.correct_questions)
            self.removed.append(question)
        else:
            self.correct_questions -= 1
            self.ids.correct_button.text = 'Correct'
            self.removed.remove(question)
        
class QuizOGScreen(BaseScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global current_player_data
        App.get_running_app().bind(
            color_scheme=self.update_answer_style,
            current_font=self.update_answer_style
        )         # Bind to app properties
        self.questions = []
        self.current_index = 0
        self.all_topics = json.load(open(get_json_path('kw_topics.json'), 'r'))    
        self.codes2 = ['0-4', '4-8', '8-12', '12-16', '16-20', '20-24', '24-28', '28-32', '32-36', '36-40']
        self.codes = [0, 98722, 45694, 44328, 67640, 55321, 35248, 83002, 11834, 58244]
        self.topic = ''
        self.start = True
        self.change_start = False
        self.popup = None
        # Ensure defaults exist
        if not hasattr(current_player_data, 'removed'):
            current_player_data = {
                "removed": [],
                "removed_topics": [],
                "points": 0,
                "latest_code": 0
            }
        self.code = current_player_data.get("latest_code", 0)        
        self.removed_topics = current_player_data.get('removed_topics', [])
        self.removed_list = current_player_data.get('removed', [])
        self.correct_questions = current_player_data.get('points', 0)
        topic_index = self.codes2[self.codes.index(self.code)]
        if re.findall(r'(\d{2}-\d{2})', topic_index):
            x, y = topic_index[0:2], topic_index[3:]
        else:
            x, y = topic_index[0], topic_index[2]
        try:
            self.topics = self.all_topics[int(x):int(y)]
        except:
            self.topics = self.all_topics[int(x):]
        self.topics = [topic for topic in self.topics if topic not in self.removed_topics]
        self.load_questions()

    def update_answer_style(self, *args):
        """Update answer label style dynamically"""
        app = App.get_running_app()
        answer_label = self.ids.answer_label
        answer_label.color = app.color_scheme
        answer_label.font_name = app.current_font
        
        # Force texture update
        answer_label.texture_update()

    def on_pre_enter(self, *args):
        self.code = current_player_data.get("latest_code", 0)        
        self.removed_topics = current_player_data.get('removed_topics', [])
        self.removed_list = current_player_data.get('removed', [])
        self.correct_questions = current_player_data.get('points', 0)
        topic_index = self.codes2[self.codes.index(self.code)]
        if re.findall(r'(\d{2}-\d{2})', topic_index):
            x, y = topic_index[0:2], topic_index[3:]
        else:
            x, y = topic_index[0], topic_index[2]
        try:
            self.topics = self.all_topics[int(x):int(y)]
        except:
            self.topics = self.all_topics[int(x):]
        self.topics = [topic for topic in self.topics if topic not in self.removed_topics]
        self.load_questions()

    def level_popup(self):
        self.correct_questions -= 100
        app = App.get_running_app()
        self.code = self.codes[self.codes.index(self.code)+1]
        global current_player_data
        current_player_data['latest_code'] = self.code
        code_label_text = f'You leveled up! Good job! Your code: {self.code}.'
        code_label = Label(
            text=code_label_text,
            font_size=40,
            font_name= app.current_font,
            color= app.color_scheme,
            size_hint_y=0.2
        )
        content = BoxLayout(orientation='vertical', spacing=20, padding=20)
        content.add_widget(code_label)
        btn = Button(
            text='ok',
            font_size=50,
            font_name= app.current_font,
            size_hint_y=0.2,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color= app.color_scheme
        )
        content.add_widget(btn)
        self.popup = Popup(
            title='',
            title_font='zpix.ttf',
            title_size='1sp',
            title_color=[0.88, 0.47, 0.18, 1],
            content=content,
            size_hint=(0.7, 0.4),
            separator_color=[0.88, 0.47, 0.18, 1],
            background='',
            background_color=(0, 0, 0, 0.8)
        )
        btn.bind(on_press=self.copy_code)
        self.popup.open()
        

    def copy_code(self, *args):
        topic_index = self.codes2[self.codes.index(self.code)]
        if re.findall(r'(\d{2}-\d{2})', topic_index):
            x, y = topic_index[0:2], (topic_index[3:] if topic_index[3:] != '40' else 'e')
        elif re.findall(r'(\d{1}-\d{2})', topic_index):
            x, y = topic_index[0], topic_index[2:]
        elif re.findall(r'(\d{1}-\d{1})', topic_index):
            x, y = topic_index[0], topic_index[2]
        else:
            print('Invalid numbers...\n\n\n\n...for now')
        try:
            self.topics = self.all_topics[int(x):int(y)]
        except:
            self.topics = self.all_topics[int(x):]
        self.topic = random.choice(self.topics)
        self.ids.topic_label.text = self.topic
        self.ids.code_input.text = ''
        self.ids.question_label.text = ''
        self.ids.answer_label.text = ''
        self.popup.dismiss()
        

    def load_questions(self):
        try:
            topic = random.choice(self.topics)
            self.ids.topic_label.text = topic
            
            topic_file = get_json_path(f'kw_{topic}.json')
            if not os.path.exists(topic_file):
                raise FileNotFoundError(f"kw_{topic}.json not found")
                    
            with open(topic_file, 'r', encoding='utf-8') as f:
                self.all_questions = json.load(f)
                self.questions = [x for x in self.all_questions if x[0] not in self.removed_list]
                if len(self.questions) >= 10:
                    self.questions = random.sample(self.questions, k=10)
                else:
                    if not self.questions:
                        self.load_questions()
                    else:    
                        random.shuffle(self.questions)
                self.current_index = 0
                self.show_question()
        except Exception as e:
            pass

    def verify(self):
        global current_player_data
        if self.ids.code_input.text:
            try:
                supplied_code = int(self.ids.code_input.text)
            except:
                print('Number only.')
                return
        else:
            supplied_code = 0
        if supplied_code in self.codes: # if input code exists, update player code
            current_player_data['latest_code'] = supplied_code
            topic_index = self.codes2[self.codes.index(supplied_code)]
            self.ids.code_input.text='accepted' # show loaded if no such code
        else:
            self.ids.code_input.text='invalid' # show invalid if no such code
            return
        if re.findall(r'(\d{2}-\d{2})', topic_index):
            x, y = topic_index[0:2], topic_index[3:]
        else:
            x, y = topic_index[0], topic_index[2]
        self.topics = self.all_topics[int(x):int(y)]
        self.ids.answer_label.opacity = 0
        self.correct_questions = 0
        self.topic = random.choice(self.topics)
        self.ids.topic_label.text = self.topic
        self.ids.code_input.text = ''
        self.ids.question_label.text = ''
        self.ids.answer_label.text = ''
        self.load_questions()
    
    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = question
            self.ids.answer_label.text = answer
        else:
            self.start = True
            self.change_start = False
            self.ids.answer_input.hint_text = f"Score: {self.correct_questions}"
            self.on_pre_enter()

    def toggle_answer(self):
        if self.ids.answer_label.opacity == 0:
            self.ids.answer_label.opacity = 1
        else:
            self.ids.answer_label.opacity = 0

    def next_question(self):
        self.current_index += 1
        self.ids.answer_label.opacity = 0
        self.ids.correct_button.text = 'Correct'
        self.ids.answer_input.text = ''
        self.ids.answer_input.hint_text = f'Score: {self.correct_questions}'
        if self.correct_questions >= 100:
            self.level_popup()
        self.show_question()

    def back_to_root(self):
        global current_player_data, full_player_data, current_player_name
        
        if current_player_name:  # Only save if logged in
            current_player_data.update({
                'points': self.correct_questions,
                'removed': self.removed_list,
                'removed_topics': self.removed_topics
            })
            full_player_data[current_player_name] = current_player_data
            
            try:
                player_file = get_json_path('kw_gui_players.json')
                json.dump(full_player_data, open(player_file, 'w'))
            except Exception as e:
                print(f"Error saving player data: {e}")

        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'

        sm = self.manager       # Access the screen manager
        sm.transition = SlideTransition(direction='right')       # Set transition direction
        sm.current = 'menu'         # Change screen

    def mark_correct(self):
        question = str(self.ids.question_label.text)
        if self.ids.correct_button.text == 'Correct':
            self.correct_questions += 1
            self.removed_list.append(question)
            self.ids.correct_button.text = str(self.correct_questions)
        else:
            self.correct_questions -= 1
            self.removed_list.remove(question)
            self.ids.correct_button.text = 'Correct'

class StudyScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_dir = get_data_path()  # Modified to use our data path function
        self.new_dir = ""
        os.makedirs(self.data_dir, exist_ok=True)
        files = [f[:-4] for f in os.listdir(self.data_dir) if f.endswith('.txt')]
        self.ids.file_spinner.values = sorted(files) if files else ["No .txt files found"]         
    
    def update_spinner(self):
        files = [f[:-4] for f in os.listdir(self.data_dir) if f.endswith('.txt')]
        self.ids.file_spinner.values = sorted(files) if files else ["No .txt files found"] 
        self.ids.file_spinner.text = ''
        self.ids.filename_input.text = ''
        self.ids.content_input.text = ''
        self.ids.save_button.text = 'Save'

    def change_dir(self, dir_name):
        self.ids.file_spinner.text = ''
        self.new_dir = os.path.join(self.data_dir, dir_name)
        os.makedirs(self.new_dir, exist_ok=True)
        self.show_message(f".{str(self.new_dir)[33:]} selected")
        files = [f[:-4] for f in os.listdir(self.new_dir) if f.endswith('.txt')]
        self.ids.file_spinner.values = sorted(files) if files else ["No .txt files found"] 
        
    def load_file(self):
        self.ids.content_input.text = ''
        filename = self.ids.file_spinner.text.strip()   
        if not filename:
            self.show_error("Please enter a filename")
        else:               
            if not filename.endswith('.txt'):
                filename += '.txt'            
            filepath = os.path.join(self.new_dir if self.new_dir else self.data_dir, filename)       
            try:
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.ids.content_input.text = content
                    self.ids.save_button.text = f'Save [{filename[:-4]}]'
                else:
                    self.ids.content_input.text = ""
                self.show_message(f"{'Loaded' if os.path.exists(filepath) else 'Created'} @{str(filepath)[33:]}")
            except Exception as e:
                self.show_error(f"Error: {str(e)}")

    def create_file(self):
        self.ids.content_input.text = '' # clear content from previous load
        filename = self.ids.filename_input.text.strip() # get file name from create first      
        if not filename: # make sure there is a file name on screen
            self.show_error("Please enter a filename")
        else:               
            if not filename.endswith('.txt'): # Ensure .txt extension
                filename += '.txt'
            if not self.new_dir:     # ensure the new file is created in the correct directory
                filepath = os.path.join(self.data_dir, filename) 
            else:
                filepath = os.path.join(self.new_dir, filename)         
            try:
                if os.path.exists(filepath): # loads existing file if matches new file name
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    self.ids.content_input.text = content
                    self.ids.save_button.text = f'Save [{filename[:-4]}]'  # removes .txt
                else:
                    self.ids.content_input.text = ""
                    self.ids.save_button.text = f'Save [{filename[:-4]}]'  # removes .txt
                self.show_message(f"{'Loaded' if os.path.exists(filepath) else 'Created'} @{str(filepath)[33:]}") # show which folder selected
            except Exception as e:
                self.show_error(f"Error: {str(e)}")
    

    def save_file(self):
        if self.ids.save_button.text == 'Save':
            self.show_error("Please enter a filename")
            return
        else:
            filename = self.ids.save_button.text[6:-1]
        content = self.ids.content_input.text
        if not filename.endswith('.txt'):
            filename += '.txt'
        filepath = os.path.join(self.new_dir if self.new_dir else self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.show_message(f"Saved @{str(filepath)[33:]}")
        except Exception as e:
            self.show_error(f"Error saving file: {str(e)}")

        self.update_spinner()

    def show_message(self, message):
        self.ids.status_label.text = message
        self.ids.status_label.color = (0, 1, 0, 1)  # Green for success
        Animation(opacity=1, duration=0.3).start(self.ids.status_label)
        Clock.schedule_once(lambda dt: Animation(opacity=0, duration=3).start(self.ids.status_label), 3)

    def show_error(self, message):
        self.ids.status_label.text = message
        self.ids.status_label.color = (1, 0, 0, 1)  # Red for error
        Animation(opacity=1, duration=0.3).start(self.ids.status_label)
        Clock.schedule_once(lambda dt: Animation(opacity=0, duration=3).start(self.ids.status_label), 3)

    def back_to_root(self):
        if self.ids.back_button.text == 'o.O':
            self.ids.back_button.text = 'O.o'
        elif self.ids.back_button.text == 'O.o':
            self.ids.back_button.text = 'x.O'
        elif self.ids.back_button.text == 'x.O':
            self.ids.back_button.text = 'O.x'
        elif self.ids.back_button.text == 'O.x':
            self.ids.back_button.text = '>.<'
        elif self.ids.back_button.text == '>.<':
            self.ids.back_button.text = 'o.O'
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'menu'

class KeyWizApp(App):
    global current_player_data
    current_bg_music = StringProperty('music1.mp3')
    current_bg_image = StringProperty('bg2.jpg')
    current_font = StringProperty('zpix.ttf')
    COLOR_SCHEMES = {
        'Dark': [0.88, 0.47, 0.18, 1],
        'Techno': [0.2, 0.6, 1, 1],
        'Dull': [0.5, 0.5, 0.5, 1]
    }
    color_scheme = ListProperty(COLOR_SCHEMES['Dark'])  # Default orange-brown

    def build(self):

        # Initialize storage and copy bundled files (if needed)
        self.setup_app_storage()

        # Load KV file with error handling
        try:
            kv_file = os.path.join(os.path.dirname(__file__), 'layout.kv')
            Builder.load_file(kv_file)
        except Exception as e:
            print(f"Error loading KV file: {e}")

        Window.clearcolor = (0.05, 0.05, 0.05, 1) 
        
        # Load music with error handling
        try:
            self.background_music = SoundLoader.load(self.current_bg_music)
            if self.background_music:
                self.background_music.loop = True
                self.background_music.play()
        except Exception as e:
            print(f"Error loading music: {e}")

        sm = ScreenManager()
        screens = [
            LoginScreen(name='login'),
            MenuScreen(name='menu'),
            DevModeScreen(name='dev_mode'),
            ToDoScreen(name='todo'),
            NotesScreen(name='notes'),
            SettingsScreen(name='settings'),
            EditTopicScreen(name='edit_topic'),
            QuizSingleScreen(name='quiz_single'),
            QuizAllScreen(name='quiz_all'), 
            QuizOGScreen(name='quiz_normal'),
            StudyScreen(name='study') 
        ]
        
        for screen in screens:
            sm.add_widget(screen)
        
        sm.current = 'login'
        return sm
    
    def setup_app_storage(self):
        """Ensure storage exists and copy bundled files."""
        storage = get_app_storage()  # Your existing function
        os.makedirs(storage, exist_ok=True)
        
        if ANDROID:
            self.copy_bundled_files()

    def copy_bundled_files(self):
        """Copy files from APK's read-only 'app/' dir to writable storage."""
        from android.storage import app_storage_path
        src_dir = os.path.join(app_storage_path(), "app")  # APK files
        dst_dir = app_storage_path()  # Writable dir
        
        files_to_copy = [
            "kw_gui_players.json",
            "kw_topics.json",
            "notes.txt",
        ]
        
        for filename in files_to_copy:
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            
            # Copy only if source exists and destination doesn't
            if os.path.exists(src_path) and not os.path.exists(dst_path):
                try:
                    import shutil
                    shutil.copy(src_path, dst_path)
                    print(f"[DEBUG] Copied {filename} to writable storage.")
                except Exception as e:
                    print(f"[ERROR] Failed to copy {filename}: {str(e)}")
    
    def update_all_screens(self):
        """Update all screens with current settings"""
        for screen in self.root.screens:
            if hasattr(screen, 'update_style'):
                screen.update_style()
    
    def update_widget_colors(self, widget):
        """Recursively update colors for widget and its children"""
        if hasattr(widget, 'color'):
            # Skip special labels that shouldn't change color
            if not hasattr(widget, 'id') or ('error_label' not in widget.id and 'answer_label' not in widget.id):
                widget.color = self.color_scheme
        
        # Update canvas instructions
        if hasattr(widget, 'canvas'):
            self.update_canvas_colors(widget.canvas)
            if hasattr(widget, 'canvas_before'):
                self.update_canvas_colors(widget.canvas.before)
            if hasattr(widget, 'canvas_after'):
                self.update_canvas_colors(widget.canvas.after)
        
        # Recursively update children
        if hasattr(widget, 'children'):
            for child in widget.children:
                self.update_widget_colors(child)
    
    def update_canvas_colors(self, canvas):
        """Update color instructions in a canvas"""
        # We can't iterate directly, so we need to handle this differently
        # The background updates are already handled in update_all_screens
        pass

    def change_music(self, music_file):
        global current_player_data
        current_player_data['music'] = music_file
        if self.background_music:
            self.background_music.stop()
        self.current_bg_music = music_file
        self.background_music = SoundLoader.load(music_file)
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()

    def change_quotes(self, quote_file):
        global QUOTES, current_player_data
        if quote_file == "clap":
            QUOTES = CLAP[:]
        elif quote_file == "slap":
            QUOTES = SLAP[:]
        elif quote_file == "flap":
            QUOTES = FLAP[:]
        current_player_data['quotes'] = quote_file
    
    def change_color_scheme(self, scheme_name):
        global current_player_data
        current_player_data['color'] = scheme_name
        self.color_scheme = self.COLOR_SCHEMES.get(scheme_name, [0.88, 0.47, 0.18, 1])
        for screen in self.root.screens:
            if hasattr(screen, 'update_child_colors'):
                screen.update_child_colors()
    
    def change_bg_image(self, image_file):
        """Change background image for all screens"""
        # Verify the file exists first
        global current_player_data
        current_player_data['background'] = image_file
        if not os.path.exists(image_file):
            print(f"Error: Background image {image_file} not found!")
            return
            
        self.current_bg_image = image_file
        self.update_all_screens()

    def change_font(self, font_file):
        global current_player_data
        current_player_data['font'] = font_file
        self.current_font = font_file
        # Force refresh all screens
        for screen in self.root.screens:
            for child in screen.walk():
                if hasattr(child, 'font_name'):
                    child.font_name = font_file
    
    def load_player_settings(self):
        global current_player_data
        self.current_bg_image = current_player_data['background']
        self.current_bg_music = current_player_data['music']
        self.current_font = current_player_data['font']
        self.color_scheme = self.COLOR_SCHEMES[current_player_data['color']]
        self.change_quotes(current_player_data['quotes'])
        self.change_music(self.current_bg_music)
        self.change_bg_image(self.current_bg_image)
        self.change_font(self.current_font)
                    

if __name__ == '__main__':
    try:
        APP = KeyWizApp()
        APP.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        # Attempt to save crash log
        try:
            crash_log = get_json_path('crash_log.txt')
            with open(crash_log, 'a') as f:
                f.write(f"{datetime.now()}: {str(e)}\n")
        except:
            pass