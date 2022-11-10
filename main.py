import os
import pygame

from kivy.core.window import Window
from kivy.properties import StringProperty, Clock, BooleanProperty, ColorProperty, ObjectProperty, DictProperty, \
    NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from pynput import keyboard
from pynput.keyboard import Listener
from kivymd.app import MDApp


class MainWidget(RelativeLayout):
    music_dir = r'C:\Users\Razor\Music'
    music_path = StringProperty()
    list_of_files = []
    center_button = StringProperty(r'play')
    center_button_state = BooleanProperty(False)

    text = StringProperty('testing')

    # apps color scheme.
    background = ColorProperty("#36575c")
    primary = ColorProperty([0, 0, 0, 0.8])
    secondary = ColorProperty("#484a4a")
    # [0, 0, 0, 0.6]

    music_obj = ObjectProperty(None)

    song_list1 = DictProperty()# list of the songs dir and pos for loading files.
    song_list2 = DictProperty()# list of files names to append to the button.

    index_pos = NumericProperty(0)# the index position of the song that's playing
    length_of_list = NumericProperty(0)# the length of the list to allow for cycling of the list

    play_state = NumericProperty(0)# to check if the song needs to start or paused or unpaused
    music_volume = NumericProperty(1)# volume of the music
    progressbar = ObjectProperty()# the value of the progressbar

    music_length = NumericProperty(0)# the length of the song
    music_curr_pos = NumericProperty(0)# the positioning of the song
    songs_vol = NumericProperty(0)
    song_num = NumericProperty(0)

    def __init__(self, **kwargs) -> None:
        super(MainWidget, self).__init__(**kwargs)
        pygame.mixer.init()# initiates the pygame mixer method
        self.load_files()
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        Clock.schedule_interval(self.update, 1.0/15)

    def load_files(self) -> None:
        num = 0

        layout2 = GridLayout(cols=1, spacing=0, size_hint_y=None)# creates a gridlayout to add the buttons into
        layout2.bind(minimum_height=layout2.setter('height'))# not sure how it works but makes the scrollview work

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

                        btn = Button(text=self.song_list1[self.length_of_list], size_hint_y=None, height=40,
                                     background_color=self.primary, on_press=(lambda x, y=num: self.screen_press(y)))
                        #appends the button to the grid layout.
                        layout2.add_widget(btn)
                        num += 1
                        self.length_of_list += 1

        # creates a scrollview to add the grid too.
        main_window = ScrollView(size_hint=(1, .86), size=(Window.width, Window.height),
                                 do_scroll_x=False, do_scroll_y=True, scroll_timeout=300,
                                 scroll_distance=100, pos_hint={'center_x': 0.5, 'center_y': 0.56})

        # adds the gird to the scrollview
        main_window.add_widget(layout2)

        # adds the scrollview to the main layout
        self.add_widget(main_window)

        # the length of te list is 1 integer to long so this removes 1
        self.length_of_list = self.length_of_list - 1
        # start the audio function

    def screen_press(self, y: int) -> None:
        if self.song_list2:
            self.song_list2 = {}
            num = 0
            for root, dir, files in os.walk(self.song_list1[y]):
                for name in files:
                    # if the file is and mp3 file it start the appending sequence
                    if name.endswith('.mp3'):
                        self.song_list2[num] = os.path.join(root, name)
                        num += 1
        else:
            num = 0
            for root, dir, files in os.walk(self.song_list1[y]):
                for name in files:
                    # if the file is and mp3 file it start the appending sequence
                    if name.endswith('.mp3'):
                        self.song_list2[num] = os.path.join(root, name)
                        num += 1
        self.load_song()

    def load_song(self) -> None:
        # print(self.song_list2[self.song_num])
        pygame.mixer.music.load(self.song_list2[self.song_num])
        pygame.mixer.music.play()
        self.play_state = 1
        self.center_button = 'pause'
        self.center_button_state = True

    def play_pause_state(self) -> None:
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
            self.text = "playing"

    def next(self) -> None:
        if self.song_list2:
            if self.song_num == len(self.song_list2)-1:
                self.song_num = 0
                self.play_state = 1

                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                pygame.mixer.music.play()

                self.center_button = 'pause'
            else:
                self.song_num += 1
                self.play_state = 1

                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                pygame.mixer.music.play()

                self.center_button = 'pause'
        else:
            print("list not loaded")

    def previous(self) -> None:
        if self.song_list2:
            if self.song_num == 0:
                self.song_num = len(self.song_list2) - 1
                self.play_state = 1

                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                pygame.mixer.music.play()
                self.center_button = "pause"
            else:
                self.song_num -= 1
                self.play_state = 1

                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.song_list2[self.song_num])
                pygame.mixer.music.play()
                self.center_button = "pause"
        else:
            self.text = "list not loaded"

    def on_press(self, key):
        if str(key) == 'Key.media_play_pause':
            self.play_pause_state()
        if str(key) == 'Key.media_next':
            self.next()
        if str(key) == 'Key.media_previous':
            self.previous()
        if str(key) == 'Key.f10':
            self.vol_up()
        if str(key) == 'Key.f10':
            self.vol_down()

    def on_release(self, key):
        if key == keyboard.Key.esc:
            return False


    def vol_up(self):
        vol = self.ids.slider.value/100
        vol += 0.01
        self.ids.slider.value = vol*100

    def vol_down(self):
        vol = self.ids.slider.value/100
        vol -= 0.01
        self.ids.slider.value = vol*100

    def set_vol(self, volume: int) -> None:
        pygame.mixer.music.set_volume(volume)


    def update(self, dt: float) -> None:
        if self.play_state == 1:
            self.set_vol(self.ids.slider.value/100)
            if not pygame.mixer.music.get_busy():
                self.next()


class WindowsplayerApp(MDApp):
    pass


WindowsplayerApp().run()