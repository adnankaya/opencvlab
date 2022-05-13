import sys
import json
import tkinter as tk
# internals
from settings import base
from .settings_widget import SettingsWidget


class SettingsFrame(SettingsWidget):
    def __init__(self, *args, **kwargs):
        SettingsWidget.__init__(self, *args, **kwargs)
        self.def_cam_var = tk.StringVar(self.labelframe_default_camera)
        self.rb_webcam.configure(variable=self.def_cam_var, value='webcam')
        self.rb_external_camera.configure(variable=self.def_cam_var, value='external')
        self.def_cam_var.set(base.SETTINGS['default_camera'])
        # Combobox camera list values
        platform = sys.platform.lower()
        if platform.startswith('linux'):
            from settings import linux as myos
        if platform.startswith('win'):
            from settings import windows as myos
        self.combobox_cameralist.configure(values=myos.CAMLIST)
        self.combobox_cameralist.set(base.SETTINGS['selected_camera'])
        # theme
        self.combobox_theme.configure(values=base.THEMELIST)
        self.combobox_theme.set(base.SETTINGS['selected_theme'])

    def select_default_camera(self):
        var = self.def_cam_var.get()
        with open(base.SETTINGS_FILE, 'w') as settingsfile:
            base.SETTINGS['default_camera'] = var
            json.dump(base.SETTINGS, settingsfile)

    def select_camera(self, event=None):
        var = self.combobox_cameralist.get()
        with open(base.SETTINGS_FILE, 'w') as settingsfile:
            base.SETTINGS['selected_camera'] = var
            json.dump(base.SETTINGS, settingsfile)

    def select_theme(self, event=None):
        var = self.combobox_theme.get()
        with open(base.SETTINGS_FILE, 'w') as settingsfile:
            base.SETTINGS['selected_theme'] = var
            json.dump(base.SETTINGS, settingsfile)
        tk.messagebox.showinfo("You changed the theme",
                               'Restart to see the changes')
