import json
import os

import pygame
from kivy.core import window

from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, BooleanProperty, ColorProperty, ObjectProperty, DictProperty, \
    NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from settingsjson import settings_json

from CustomSettings import CustomSettings


class Error_windows(RelativeLayout):
    """Not being used yet"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Music_folders(Screen):
    # creates a gridlayout to add the buttons into
    layout2 = GridLayout(cols=1, spacing=0, size_hint_y=None)
    # not sure how it works but makes the scrollview work
    layout2.bind(minimum_height=layout2.setter('height'))

    def __int__(self):
        self.width = Window.width
        self.height = Window.height
        self.but = MDRectangleFlatButton(
            text="test", size_hint=(self.width, self.width), height=40,)
        self.layout2.add_widget(self.but)

    def add(self, widget):
        self.layout2.add_widget(widget)

    def add_scrowl_view(self):
        # creates a scrollview to add the grid too.
        main_window = ScrollView(size_hint=(1, .86), size=(Window.width, Window.height),
                                 do_scroll_x=False, do_scroll_y=True, scroll_timeout=300,
                                 scroll_distance=100, pos_hint={'center_x': 0.5, 'center_y': 0.56})

        # adds the gird to the scrollview
        main_window.add_widget(self.layout2)

        # adds the scrollview to the main layout
        self.add_widget(main_window)


class WindowsplayerApp(MDApp):
    def build(self) -> None:
        """sets the name and icon of the app"""
        self.title = "Wmusic player"
        self.icon = r'assets\fox.png'
        # self.settings_cls = SettingsWithSidebar()

    def build_config(self, config) -> None:
        """builds a default settings menu and assigns it values"""
        config.setdefaults("settings panel one", {
            "bool": False,
            "numeric": 5,
            "option": "option2",
            "string": "user",
            "path": "C:\\Users\\Public\\Music"})

    def build_settings(self, settings) -> None:
        """gets data from the settings_json and configures the look of the window"""
        settings.add_json_panel(
            "Main settings", self.config, data=settings_json)

    def on_config_change(self, config, section, key, value) -> None:
        """gets the data from the settings menu and writes them to a file"""
        dicts = {"add_play_lists": f"{self.config.get('settings panel one', 'bool')}",
                 "music_dir": f"{self.config.get('settings panel one', 'path')}",
                 "volume": str(self.config.get('settings panel one', 'numeric')),
                 "options": f"{self.config.get('settings panel one', 'option')}",
                 "string": self.config.get('settings panel one', "string"), }
        json_object = json.dumps(dicts, indent=3)
        with open('get_setting.json', "w+") as file:
            file.write(json_object)
        # pass


if __name__ == '__main__':
    array = ["⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠜⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⠿⠿⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣿",
             "⣿⣿⡏⠁⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⡄⠀⠀⠀⠀⢀⣴⣿⣿⣿",
             "⣿⣿⣷⣄⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡧⠇⢀⣤⣶⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣾⣮⣭⣿⡻⣽⣒⠀⣤⣜⣭⠐⢐⣒⠢⢰⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⣏⣿⣿⣿⣿⣿⣿⡟⣾⣿⠂⢈⢿⣷⣞⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣿⣷⣶⣾⡿⠿⣿⠗⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠻⠋⠉⠑⠀⠀⢘⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⣿⡿⠟⢹⣿⣿⡇⢀⣶⣶⠴⠶⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⣿⣿⣿⡿⠀⠀⢸⣿⣿⠀⠀⠣⠀⠀⠀⠀⠀⡟⢿⣿⣿⣿⣿⣿⣿⣿⣿",
             "⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠹⣿⣧⣀⠀⠀⠀⠀⡀⣴⠁⢘⡙⣿⣿⣿⣿⣿⣿⣿",
             "⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⠗⠂⠄⠀⣴⡟⠀⠀⡃ ⣿⣿⣿⣿⣿⣿"]
    for i in array:
        print(i)

    WindowsplayerApp().run()

# TODO: add a top bar with the options button
# add a custom font
