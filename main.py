import json
import os

import pygame
from kivy.config import ConfigParser

from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, BooleanProperty, ColorProperty, ObjectProperty, DictProperty, \
    NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import *
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from pynput import keyboard
from kivymd.app import MDApp
from settingsjson import settings_json


class CustomSettings(SettingsWithSidebar):
    def __int__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.config = ConfigParser()
        self.config.read("appconfig.ini")

    def build_config(self):
        s = SettingsWithSidebar()
        s.add_json_panel('Custom panel', self.config, data=settings_json)


class Error_windows(RelativeLayout):
    """Not being used yet"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


"The apps main window"


class MainWidget(RelativeLayout):
    append_list = ObjectProperty(False)
    main_window = ObjectProperty()

    music_dir = r'C:\Users\Public\Music'
    get_music_path = StringProperty()
    music_path = StringProperty()
    list_of_files = []
    folder_name = ''

    center_button = StringProperty(r'play')
    center_button_state = BooleanProperty(False)
    text = StringProperty('testing')

    # apps color scheme.
    background = ColorProperty("#36575c")
    primary = ColorProperty([0, 0, 0, 0.8])
    secondary = ColorProperty("#484a4a")

    music_obj = ObjectProperty(None)
    song_list1 = DictProperty()  # list of the songs dir and pos for loading files.
    song_list2 = DictProperty()  # list of files names to append to the button.

    index_pos = NumericProperty(0)  # the index position of the song that's playing
    length_of_list = NumericProperty(0)  # the length of the list to allow for cycling of the list

    play_state = NumericProperty(0)  # to check if the song needs to start or paused or unpaused
    music_volume = NumericProperty(1)  # volume of the music
    progressbar = ObjectProperty()  # the value of the progressbar

    music_length = NumericProperty(0)  # the length of the song
    folder_num = NumericProperty(0)  # the positioning of the song
    songs_vol = NumericProperty(0)
    volume = NumericProperty(5)
    song_num = NumericProperty(0)

    def __init__(self, **kwargs) -> None:
        self.alert = None
        super(MainWidget, self).__init__(**kwargs)
        pygame.mixer.init()  # initiates the pygame mixer method for playing the music
        self.get_music_path = self.get_settings()
        self.load_files()
        # listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        # listener.start()
        Clock.schedule_interval(self.update, 1.0/1.0)
        Clock.schedule_interval(self.setInterval, 1)

    def show(self) -> None:
        """this is for testing screens"""
        setting_menu = CustomSettings()

        self.add_widget(setting_menu)

    def get_settings(self) -> str:
        try:
            with open('get_setting.json', 'r') as file:
                dic = json.loads(file.read())

            self.music_dir = dic["music_dir"]
            self.volume = int(dic['volume'])
            if dic['add_play_lists'] == '1':
                self.append_list = True
        except Exception as error:
            print(error)

        return self.music_dir

    def error(self, error: str) -> None:
        """gets an argument and creates a popup window that displays the error int a box"""
        if self.alert:
            pass
        else:
            self.alert = MDDialog(text=str(error), radius=[20, 20, 20, 20],
                                  buttons=[MDFlatButton(text="Dismiss", on_press=lambda x: self.alert.dismiss())])
            self.alert.open()

    def load_files(self) -> None:
        """
            searches the directory's with the os.walk() and creates a dictionary of the folders with all the mp3 in it
            stores the keys of all the folders in a button and loads it into a scrollview
            I use a lambda func to store the keys in the button
            """
        num = 0

        self.layout2 = GridLayout(cols=1, spacing=0, size_hint_y=None)  # creates a gridlayout to add the buttons into
        self.layout2.bind(minimum_height=self.layout2.setter('height'))  # not sure how it works but makes the scrollview work

        # uses the os.walk to search through the directory
        for root, dir, files in os.walk(self.music_dir):
            for name in files:
                # if the file is and mp3 file it start the appending sequence
                if name.endswith('.mp3'):
                    self.music_path = os.path.join(root)
                    if self.music_path in self.list_of_files:
                        pass
                    else:
                        self.list_of_files.append(self.music_path)
                        self.song_list1[self.length_of_list] = root

                        file_name = self.song_list1[self.length_of_list].split('\\')
                        # return str(file_name[-1].strip('.mp3'))

                        self.btn = Button(text=file_name[-1], size_hint_y=None, height=40,
                                     background_color=self.primary, on_press=(lambda x, y=num: self.screen_press(y)))
                        # appends the button to the grid layout.
                        self.layout2.add_widget(self.btn)
                        num += 1
                        self.length_of_list += 1

        # creates a scrollview to add the grid too.
        self.main_window = ScrollView(size_hint=(1, .86), size=(Window.width, Window.height),
                                 do_scroll_x=False, do_scroll_y=True, scroll_timeout=300,
                                 scroll_distance=100, pos_hint={'center_x': 0.5, 'center_y': 0.56})

        # adds the gird to the scrollview
        self.main_window .add_widget(self.layout2)

        # adds the scrollview to the main layout
        self.add_widget(self.main_window)

        # the length of te list is 1 integer to long so this removes 1
        self.length_of_list = self.length_of_list - 1
        # start the audio function

    def re_load_files(self) -> None:
        for i in range(len(self.layout2.children)):
            del self.layout2.children[0]

        self.song_list1 = []
        self.length_of_list = 0
        self.list_of_files = []
        self.load_files()

    def screen_press(self, y: int) -> None:
        """
            this is the button func that's called by the lambda and takes the argument from it.
            first it checks if a playlist has already been created and clears it if it has.
            then it takes the keys and gets the dir then os.walk() to search for the .mp3 files.
            and creates a playlist that stores the paths for the songs.
            then calls the load_song() function
            """
        self.folder_name = y
        if not self.append_list:
            if self.song_list2:
                self.song_list2 = {}

        num = 0
        for root, dir, files in os.walk(self.song_list1[self.folder_name]):
            for name in files:
                # if the file is and mp3 file it start the appending sequence
                if name.endswith('.mp3'):
                    self.song_list2[num] = os.path.join(root, name)
                    num += 1
        self.load_song()

    def get_song_name(self) -> str:
        """
        filters the song path to get te songs name
        """
        file_name = self.song_list2[self.song_num].split('\\')
        return str(file_name[-1].strip('.mp3'))

    def load_song(self) -> None:
        """
            try's to load the first song of the playlist into the mixer and the plays it
            if it fails it calls the error function and loads the nest song in the playlist
            """
        self.song_num = 0
        try:
            pygame.mixer.music.load(self.song_list2[self.song_num])
            self.text = self.get_song_name()
            pygame.mixer.music.play()
        except Exception as error:
            self.error(error)
        self.play_state = 1
        self.center_button = 'pause'
        self.center_button_state = True

    def play_pause_state(self) -> None:
        """
        checks the play state the either to pause,play,unpause
        """
        if self.song_list2:
            if self.play_state == 0:
                pygame.mixer.music.play()

                # changes the center button to pause icon when playing
                self.center_button = 'pause'
                self.center_button_state = True
                self.play_state += 1

            elif self.play_state == 1:
                # changes the center button to pause icon when playing
                pygame.mixer.music.pause()
                self.center_button = 'play'
                self.center_button_state = False
                self.play_state += 1
            else:
                pygame.mixer.music.unpause()
                self.center_button = 'pause'
                self.center_button_state = True
                self.play_state -= 1
        else:
            self.text = "Playlist empty"

    def next(self) -> None:
        """
        checks it your at the end of the playlist and either adds one yo the index and plays next song.
        or it at the end of the list and sets te index back to 0 and restarts teh playlist
        """
        if self.song_list2:
            if self.song_num == len(self.song_list2) - 1:
                self.song_num = 0
            else:
                self.song_num += 1

            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                self.text = self.get_song_name()
                pygame.mixer.music.play()
                self.play_state = 1
            except Exception as error:
                self.error(error)
            self.center_button = 'pause'

        else:
            self.text = "Playlist empty"


    def previous(self) -> None:
        """
        checks it your at the start of the playlist and either set the index to the length of the list to start the last song.
        or it removes -1 from the index and loads the previous song.
        """
        if self.song_list2:
            if self.song_num == 0:
                self.song_num = len(self.song_list2) - 1
            else:
                self.song_num -= 1

            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                self.text = self.get_song_name()
                pygame.mixer.music.play()
                self.play_state = 1
            except Exception as error:
                self.song_num -= 2
                self.error(error)
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                self.text = self.get_song_name()
                pygame.mixer.music.play()
        else:
            self.text = "list not loaded"

    # def on_press(self, key):
    #     if str(key) == 'Key.media_play_pause':
    #         self.play_pause_state()
    #     if str(key) == 'Key.media_next':
    #         self.next()
    #     if str(key) == 'Key.media_previous':
    #         self.previous()
    #     if str(key) == 'Key.f10':
    #         self.vol_up()
    #     if str(key) == 'Key.f10':
    #         self.vol_down()

    # @staticmethod
    # def on_release(key):
    #     if key == keyboard.Key.esc:
    #         return False


    def vol_up(self) -> None:
        """
            gets the volume of the slider increases the slider by one
            """
        vol = self.ids.slider.value / 100
        vol += 0.01
        self.ids.slider.value = vol * 100


    def vol_down(self) -> None:
        """
            gets the volume of the slider decreases the slider by one
            """
        vol = self.ids.slider.value / 100
        vol -= 0.01
        self.ids.slider.value = vol * 100


    @staticmethod
    def set_vol(volume: int) -> None:
        """
        this is updates once every second.
        gets the volume of the slider decreases or increases it
        """
        pygame.mixer.music.set_volume(volume)


    def setInterval(self, dt: float) -> None:
        self.get_settings()
        # self.re_load_files()
        if self.get_music_path != self.music_dir:
            self.re_load_files()
            self.get_music_path = self.music_dir
            print("updated")

    def update(self, dt: float) -> None:
        """
        this is called every second.
        checks if the song is playing or if its over calls the next function
        """
        if self.play_state == 1:
            self.set_vol(self.ids.slider.value / 100)
            if not pygame.mixer.music.get_busy():
                self.next()


class WindowsplayerApp(MDApp):
    def build(self) -> None:
        self.title = "Wmusic player"
        self.icon = r'assets\fox.png'
        # self.settings_cls = SettingsWithSidebar()

    def build_config(self, config) -> None:
        config.setdefaults("settings panel one", {
            "bool": False,
            "numeric": 5,
            "option": "option2",
            "string": "user",
            "path": "C:\\Users\\Public\\Music"})

    def build_settings(self, settings) -> None:
        settings.add_json_panel(
            "Main settings", self.config, data=settings_json)

    def on_config_change(self, config, section, key, value) -> None:
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
    WindowsplayerApp().run()
