from kivy.uix.settings import SettingsWithSidebar
from kivy.config import ConfigParser

from kivy.uix.settings import *
from settingsjson import settings_json


class CustomSettings(SettingsWithSidebar):
    """Not being used yet"""

    def __int__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.config = ConfigParser()
        self.config.read("appconfig.ini")

    def build_config(self):
        s = SettingsWithSidebar()
        s.add_json_panel('Custom panel', self.config, data=settings_json)