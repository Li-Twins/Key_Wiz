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
from quotes import QUOTES

#!/usr/bin/python
# -*- coding: utf-8 -*-

class BaseScreen(Screen):
    current_date = StringProperty() 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_pre_enter=self.update_style)
        self.bind(size=self._update_rect, pos=self._update_rect)
        
        # Initialize canvas elements
        with self.canvas.before:
            # Background image (drawn first)
            self.bg_image = Rectangle(source='', pos=self.pos, size=self.size)
            # Semi-transparent overlay (drawn on top of image)
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
        # Update background image
        self.bg_image.source = app.current_bg_image
        # Force reload of the image
        self.bg_image.source = ''
        self.bg_image.source = app.current_bg_image

class SettingsScreen(BaseScreen):
    def back_to_root(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'menu'
    
class PasscodeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.correct_passcode = "6969"  # Default passcode, you can change this
        self.attempts = 0
        self.max_attempts = 3

    def verify_passcode(self):
        entered_passcode = self.ids.passcode_input.text
        if entered_passcode == self.correct_passcode:
            self.manager.current = 'menu'
            self.ids.passcode_input.text = ''
            self.attempts = 0
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.show_error("Max attempts reached! Exiting...")
                Clock.schedule_once(lambda dt: App.get_running_app().stop(), 2)
            else:
                self.show_error(f"Wrong passcode! {self.max_attempts - self.attempts} attempts left")
            self.ids.passcode_input.text = ''

    def show_error(self, message):
        self.ids.error_label.text = message
        Animation(opacity=1, duration=0.3).start(self.ids.error_label)
        Clock.schedule_once(lambda dt: Animation(opacity=0, duration=1).start(self.ids.error_label), 3)

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
        self.notes_file = os.path.join(App.get_running_app().user_data_dir, 'notes.txt')
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.load_notes()
    
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
                self.notes = [line.strip() for line in f.readlines() if line.strip()]
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = []
                
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
                print(f"Error saving note: {e}")
                
    def show_error_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(
            text=message,
            font_name='zpix.ttf',
            font_size=20,
            color=(0.88, 0.47, 0.18, 1)
        ))
        
        btn = Button(
            text='OK',
            size_hint=(1, 0.3),
            font_name='zpix.ttf',
            font_size=20,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.88, 0.47, 0.18, 1)
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
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'menu'

class DevModeScreen(BaseScreen):
    show_answer = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(show_answer=self.update_answer_visibility)
        # Bind to app properties
        App.get_running_app().bind(
            color_scheme=self.update_answer_style,
            current_font=self.update_answer_style
        )
        self.questions = []
        self.current_index = 0
        self.topics = []
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
            with open('kw_topics.json', 'r') as f:
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
                
            if not os.path.exists(f'kw_{topic}.json'):
                raise FileNotFoundError(f"kw_{topic}.json not found")
                
            with open(f'kw_{topic}.json', 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
                random.shuffle(self.questions)
                self.current_index = 0
                self.show_question()
                
        except:
            pass

    def show_question(self):
        if self.current_index < len(self.questions):
            question, answer = self.questions[self.current_index]
            self.ids.question_label.text = question
            self.ids.answer_label.text = answer
            self.show_answer = False  # Reset visibility
            # Update style immediately
            #self.update_answer_style()
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
        self.separator_color = (0.88, 0.47, 0.18, 1)  # Orange-brown separator
        self.title_color = (0.88, 0.47, 0.18, 1)  # Orange-brown title
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
            foreground_color=(0.88, 0.47, 0.18, 1),
            cursor_color=(0.88, 0.47, 0.18, 1),
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
            color=(0.88, 0.47, 0.18, 1)
        )
        
        # Cancel button
        cancel_btn = Button(
            text='Cancel',
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.88, 0.47, 0.18, 1)
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
                Color(0.88, 0.47, 0.18, 1)
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
            Color(0.88, 0.47, 0.18, 1)
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

    def quit(self):
        sys.exit()

class QuizScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.codes = {'5-8':'73113'}  # Example: code '73113' will access topics index 5-8
        self.topics = json.load(open('kw_topics.json', 'r'))  # Will be populated from DevModeScreen's topics

    def verify_code(self):
        code = self.ids.code_input.text.strip()
        if code in self.codes.values():
            # Find which key matches this code
            key = [k for k, v in self.codes.items() if v == code][0]
            
            # Use regex to extract indices from key (like '0-4')
            match = re.match(r'(\d+)-(\d+)', key)
            if match:
                start_idx = int(match.group(1))
                end_idx = int(match.group(2))
                
                # Get topics from DevModeScreen
                self.topics = self.topics[start_idx:end_idx+1]  # +1 because slice is exclusive
        else:
            # If code not found, silently use first four topics
            dev_screen = self.manager.get_screen('dev_mode')
            self.topics = dev_screen.topics[:4] if len(dev_screen.topics) >= 4 else dev_screen.topics.copy()
        
        # Show available topics
        topic_list = "\n".join([t.title() for t in self.topics])
        self.show_popup("Available topics", f"\n{topic_list}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text=message,
            font_name='zpix.ttf',
            font_size=30,
            color=(0.88, 0.47, 0.18, 1)
        ))
        
        btn = Button(
            text='OK',
            size_hint=(1, 0.3),
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.88, 0.47, 0.18, 1)
        )
        
        popup = Popup(
            title=title,
            title_font='zpix.ttf',
            title_size='30sp',
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
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'menu'

class ToDoScreen(BaseScreen):
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
            subject = f"ToDo List Update - {self.current_date}"
            body = f"Completed tasks on {self.current_date}:\n\n"
            body += "\n".join(self.completed_tasks) if self.completed_tasks else "No tasks completed today"
            
            if self.insight_text:
                body += "\n\nInsight:\n" + self.insight_text
            
            # Run in a background thread
            from threading import Thread
            def send_in_background():
                try:
                    msg = MIMEText(body)
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = recipient
                    
                    # Use alternative port if needed
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
                        smtp.login(sender, password)
                        smtp.send_message(msg)
                    
                    # Show success on UI thread
                    Clock.schedule_once(lambda dt: self.show_popup("Success", "Email sent!"))
                except Exception as e:
                    Clock.schedule_once(lambda dt: self.show_popup("Error", f"Failed: {str(e)}"))
            
            Thread(target=send_in_background).start()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to prepare email: {str(e)}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(
            text=message,
            font_name='zpix.ttf',
            font_size=30,
            color=(0.88, 0.47, 0.18, 1)
        ))
        
        btn = Button(
            text='OK',
            size_hint=(1, 0.3),
            font_name='zpix.ttf',
            font_size=30,
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=(0.88, 0.47, 0.18, 1)
        )
        
        popup = Popup(
            title=title,
            title_font='zpix.ttf',
            title_size='30sp',
            title_color=[0.88, 0.47, 0.18, 1],
            content=content,
            size_hint=(0.7, 0.4),
            separator_color=[0.88, 0.47, 0.18, 1],
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
    current_bg_music = StringProperty('music.mp3')
    current_bg_image = StringProperty('bg2.jpg')
    current_font = StringProperty('zpix.ttf')
    color_scheme = ListProperty([0.88, 0.47, 0.18, 1])  # Default orange-brown
    
    # Color schemes
    COLOR_SCHEMES = {
        'Dark': [0.88, 0.47, 0.18, 1],  # Original orange-brown
        'Techno': [0.2, 0.6, 1, 1],      # Blue
        'Dull': [0.5, 0.5, 0.5, 1]       # Gray
    }
    def build(self):
        kv_file = os.path.join(os.path.dirname(__file__), 'layout.kv')
        Builder.load_file(kv_file)

        Window.clearcolor = (0.05, 0.05, 0.05, 1) 
        self.background_music = SoundLoader.load(self.current_bg_music)
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()
        
        sm = ScreenManager()
        screens = [
            PasscodeScreen(name='passcode'),
            MenuScreen(name='menu'),
            DevModeScreen(name='dev_mode'),
            QuizScreen(name='quiz_mode'),
            ToDoScreen(name='todo'),
            NotesScreen(name='notes'),
            SettingsScreen(name='settings')
        ]
        
        for screen in screens:
            sm.add_widget(screen)
        
        sm.current = 'passcode'
        return sm
    
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
        if self.background_music:
            self.background_music.stop()
        self.current_bg_music = music_file
        self.background_music = SoundLoader.load(music_file)
        if self.background_music:
            self.background_music.loop = True
            self.background_music.play()
    
    def change_color_scheme(self, scheme_name):
        self.color_scheme = self.COLOR_SCHEMES.get(scheme_name, [0.88, 0.47, 0.18, 1])
        for screen in self.root.screens:
            if hasattr(screen, 'update_child_colors'):
                screen.update_child_colors()
    
    def change_bg_image(self, image_file):
        """Change background image for all screens"""
        # Verify the file exists first
        if not os.path.exists(image_file):
            print(f"Error: Background image {image_file} not found!")
            return
            
        self.current_bg_image = image_file
        self.update_all_screens()

    def change_font(self, font_file):
        self.current_font = font_file
        # Force refresh all screens
        for screen in self.root.screens:
            for child in screen.walk():
                if hasattr(child, 'font_name'):
                    child.font_name = font_file

if __name__ == '__main__':
    KeyWizApp().run()