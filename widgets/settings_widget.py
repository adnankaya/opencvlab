import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame


class SettingsWidget(ttk.Panedwindow):
    def __init__(self, master=None, **kw):
        ttk.Panedwindow.__init__(self, master, **kw)
        self.frame_buttons = ttk.Frame(self)
        self.frame_theme = ttk.Frame(self.frame_buttons)
        self.lb_default_theme = ttk.Label(self.frame_theme)
        self.lb_default_theme.config(font='{verdana} 10 {}', text='Theme')
        self.lb_default_theme.pack(side='left')
        self.combobox_theme = ttk.Combobox(self.frame_theme)
        self.combobox_theme.config(cursor='hand2', state='readonly')
        self.combobox_theme.pack(side='left')
        self.combobox_theme.bind('<<ComboboxSelected>>', self.select_theme, add='')
        self.frame_theme.config(height='200', width='200')
        self.frame_theme.pack(padx='5', pady='10', side='left')
        self.frame_buttons.config(borderwidth='2', height='50', relief='groove')
        self.frame_buttons.pack(anchor='ne', expand='false', side='right')
        self.add(self.frame_buttons, weight='1')
        self.frame_body = ttk.Frame(self)
        self.panedwindow_body = ttk.Panedwindow(self.frame_body, orient='horizontal')
        self.scrolledframe_left = ScrolledFrame(self.panedwindow_body, scrolltype='both')
        self.labelframe_default_camera = ttk.Labelframe(self.scrolledframe_left.innerframe)
        self.rb_webcam = tk.Radiobutton(self.labelframe_default_camera)
        self.rb_webcam.config(text='Webcam')
        self.rb_webcam.pack(padx='5', pady='5', side='left')
        self.rb_webcam.configure(command=self.select_default_camera)
        self.rb_external_camera = tk.Radiobutton(self.labelframe_default_camera)
        self.rb_external_camera.config(text='External')
        self.rb_external_camera.pack(padx='5', pady='5', side='left')
        self.rb_external_camera.configure(command=self.select_default_camera)
        self.labelframe_default_camera.config(height='50', text='Default Camera', width='200')
        self.labelframe_default_camera.pack(expand='false', fill='x', pady='5', side='top')
        self.frame_cameralist = ttk.Frame(self.scrolledframe_left.innerframe)
        self.combobox_cameralist = ttk.Combobox(self.frame_cameralist)
        self.combobox_cameralist.config(cursor='hand2', state='readonly')
        self.combobox_cameralist.pack(side='right')
        self.combobox_cameralist.bind('<<ComboboxSelected>>', self.select_camera, add='')
        self.label_camlist = ttk.Label(self.frame_cameralist)
        self.label_camlist.config(text='Camera List')
        self.label_camlist.pack(side='left')
        self.frame_cameralist.config(height='200', width='200')
        self.frame_cameralist.pack(fill='x', padx='5', pady='5', side='top')
        self.scrolledframe_left.configure(usemousewheel=False)
        self.scrolledframe_left.pack(expand='true', fill='both', side='top')
        self.panedwindow_body.add(self.scrolledframe_left, weight='1')
        self.scrolledframe_right = ScrolledFrame(self.panedwindow_body, scrolltype='both')
        self.canvas_1 = tk.Canvas(self.scrolledframe_right.innerframe)
        self.canvas_1.config(background='#ffffff', confine='false', height='1200', highlightbackground='#ffffff')
        self.canvas_1.config(width='1920')
        self.canvas_1.pack(anchor='center', expand='true', fill='both', side='top')
        self.scrolledframe_right.configure(usemousewheel=True)
        self.scrolledframe_right.pack(expand='true', fill='both', padx='20', pady='10', side='left')
        self.panedwindow_body.add(self.scrolledframe_right, weight='5')
        self.panedwindow_body.pack(expand='true', fill='both', side='top')
        self.frame_body.config(borderwidth='3', height='200', relief='flat', width='200')
        self.frame_body.pack(expand='true', fill='both', side='top')
        self.add(self.frame_body, weight='16')
        self.scrolledframe_5 = ScrolledFrame(self, scrolltype='both')
        self.text_1 = tk.Text(self.scrolledframe_5.innerframe)
        self.text_1.config(height='10', width='50')
        _text_ = '''settings...'''
        self.text_1.insert('0.0', _text_)
        self.text_1.pack(expand='true', fill='both', side='top')
        self.scrolledframe_5.innerframe.config(borderwidth='2', relief='raised')
        self.scrolledframe_5.configure(usemousewheel=False)
        self.scrolledframe_5.pack(side='top')
        self.add(self.scrolledframe_5, weight='2')

    def select_theme(self, event=None):
        pass

    def select_default_camera(self):
        pass

    def select_camera(self, event=None):
        pass


