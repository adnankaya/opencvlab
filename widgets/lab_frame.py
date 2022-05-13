import sys
from pathlib import Path
import json
import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

# internals
from settings import base
from .lab_widget import LabWidget
from .tooltip import CreateToolTip
from cameras.webcam import Webcam
from settings import windows as win
from helpers.functions import create_folder
from utils.tool import annot_max
# OperatingSystem
platform = sys.platform.lower()
if platform.startswith('linux'):
    from settings import linux as myos
if platform.startswith('win'):
    from settings import windows as myos


class LabFrame(LabWidget):
    def __init__(self, *args, **kwargs):
        LabWidget.__init__(self, *args, **kwargs)
        # style_global = ttk.Style()
        # style_global.theme_use(base.SETTINGS['selected_theme'])
        self.is_shotting = False
        self.is_started = False
        self.is_comparing = False
        self.image = np.zeros((100, 100), np.uint8)
        self.delay_for_img_canvas = 10
        self.frame_count = 0
        self.OUTDATA = {}
        self.img_orig_data = {}
        self.img_sample_data = {}
        # tooltip for start, stop, shot buttons
        self.create_tooltips()
        # Checkbox Original or Adjusted Frame
        self.cb_orig_adjusted_var = tk.BooleanVar(self.frame_orig_or_adjusted)
        self.cb_orig_or_adjusted.configure(variable=self.cb_orig_adjusted_var)
        # Checkbox Equalization histogram
        self.cb_equalhist_var = tk.BooleanVar(self.frame_equalizationhist)
        self.cb_equal_hist.configure(variable=self.cb_equalhist_var)
        # Checkbox Canny Edge
        self.cb_cannyvar = tk.BooleanVar(self.frame_canny)
        self.cb_canny.configure(variable=self.cb_cannyvar)
        # image Scale init value
        self.scale_orig_var = tk.IntVar(self.frame_scale_orig, value=30)
        self.scale_orig.configure(variable=self.scale_orig_var)
        self.lb_scale_o_var.configure(text=self.scale_orig_var.get())
        self.scale_sample_var = tk.IntVar(self.frame_scale_sample, value=30)
        self.scale_sample.configure(variable=self.scale_sample_var)
        self.lb_scale_s_var.configure(text=self.scale_sample_var.get())
        # Threshold Scale init value
        self.threshvar = tk.IntVar(self.frame_thresh, value=10)
        self.scale_thresh.configure(variable=self.threshvar)
        self.cb_threshvar = tk.BooleanVar(self.frame_thresh)
        self.cb_tresh.configure(variable=self.cb_threshvar)
        # Contrast
        self.contrastvar = tk.IntVar(self.frame_contrast, value=10)
        self.scale_contrast.configure(variable=self.contrastvar)
        self.cb_conrastvar = tk.BooleanVar(self.frame_contrast)
        self.cb_contrast.configure(variable=self.cb_conrastvar)
        # Brightness
        self.brightvar = tk.IntVar(self.frame_brightness, value=0)
        self.scale_bright.configure(variable=self.brightvar)
        self.cb_brightvar = tk.BooleanVar(self.frame_brightness)
        self.cb_bright.configure(variable=self.cb_brightvar)
        # Combobox kernel init values
        self.combobox_kernel.configure(values=[*base.KERNELS])
        self.combobox_kernel.set('7')
        # Combobox Threshold Types init values
        self.combobox_thresh.configure(values=base.THRESH_TYPES)
        self.combobox_thresh.set('None')
        # Combobox Colorspace init values
        self.combobox_colorspace.configure(values=base.COLORSPACES)
        self.combobox_colorspace.set('None')
        # Combobox morphological operation init values
        self.combobox_morph_opr.configure(values=base.MORPHOLOGICAL_OPERATIONS)
        self.combobox_morph_opr.set('None')
        # Combobox image gradients init values
        self.combobox_gradient.configure(values=base.IMAGE_GRADIENTS)
        self.combobox_gradient.set('None')
        # materialname
        self.materialname = tk.StringVar(self.frame_materialname)
        self.tb_materialname.configure(textvariable=self.materialname)
        self.framenumber = tk.IntVar(self.frame_framenumber, value=100)
        self.tb_framenumber.configure(textvariable=self.framenumber)
        # comparing
        self.ui_compare()
        style_pathchooser = ttk.Style()
        style_pathchooser.configure(
            'frame_path_chooser.TFrame',
            background='#808080')
        self.frame_path_chooser.config(style='frame_path_chooser.TFrame')
        # spins
        self.sb_canny_min.set('100')
        self.sb_canny_max.set('200')
        style_spin = ttk.Style()
        style_spin.configure("TSpinbox", arrowsize=20, arrowcolor="#336699")
        self.sb_canny_min.config(style='TSpinbox')

        # TODO: solve this problem
        self.combobox_gradient.config(state='disabled')

    def init_camera(self):
        with open(base.SETTINGS_FILE, 'r') as settingsfile:
            base.SETTINGS = json.load(settingsfile)
        if base.SETTINGS['default_camera'] == 'external':
            from cameras.external import External
            self.camera = External()
        else:
            try:
                self.camera = Webcam(
                    cam_source=base.SETTINGS['selected_camera']
                )
            except Exception as exc:
                self.txt_log.insert('0.0', f"{exc}\n")

    def set_frame(self, frame):
        self.frame = frame

    def get_frame(self):
        return self.frame

    def create_original_img_canvas(self, img):
        self.orig_img_canvas = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(img)
        )
        self.canvas_original.create_image(
            0, 0, image=self.orig_img_canvas, anchor=tk.NW
        )

    def upload_original(self):
        try:
            file = askopenfile(
                initialdir=myos.DATASETDIR,
                title="Select a File",
                filetypes=(
                    ("all files", "*.*"),
                    ("Text files", "*.txt*")
                )
            )
            self.orig_src = file.name
            image = cv.imread(self.orig_src)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            scaledimage = self.resize_frame(
                image,
                scale_percent=self.scale_orig_var.get()
            )
            self.create_original_img_canvas(scaledimage)

            # Change label contents
            # label_file_explorer.configure(text="File Opened: "+filename)

        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}")

    def get_scale_orig(self, event=None):
        val = self.scale_orig_var.get()
        self.lb_scale_o_var['text'] = str(val)
        image = cv.imread(self.orig_src)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        scaledimage = self.resize_frame(
            image,
            scale_percent=val
        )
        self.create_original_img_canvas(scaledimage)

    def create_sample_img_canvas(self, img):
        self.sample_img_canvas = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(img)
        )
        self.canvas_sample.create_image(
            0, 0, image=self.sample_img_canvas, anchor=tk.NW
        )

    def upload_sample(self):
        try:
            file = askopenfile(
                initialdir=myos.DATASETDIR,
                title="Select a File",
                filetypes=(
                    ("all files", "*.*"),
                    ("Text files", "*.txt*")
                )
            )
            self.sample_src = file.name
            image = cv.imread(self.sample_src)
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            scaledimage = self.resize_frame(
                image,
                scale_percent=self.scale_sample_var.get()
            )
            self.create_sample_img_canvas(scaledimage)

            # Change label contents
            # label_file_explorer.configure(text="File Opened: "+filename)
        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}")

    def get_scale_sample(self, event=None):
        val = self.scale_sample_var.get()
        self.lb_scale_s_var['text'] = str(val)
        image = cv.imread(self.sample_src)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        scaledimage = self.resize_frame(
            image,
            scale_percent=val
        )
        self.create_sample_img_canvas(scaledimage)

    def resize_frame(self, img, scale_percent=30):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        return resized

    def choose_original_data(self):
        file = askopenfile(
            initialdir=myos.MATERIALSDIR,
            title="Select Original Data File",
            filetypes=(
                ("json files", "*.json*"),
                ("all files", "*.*")
            )
        )

        orig_path = file.name
        with open(orig_path, 'r') as origfile:
            self.img_orig_data = json.load(origfile)

        self.tb_orig_data_path.config(state='active')
        self.tb_orig_data_path.delete(0, 'end')
        self.tb_orig_data_path.insert(tk.END, orig_path)
        self.tb_orig_data_path.config(state='readonly')
        if len(self.img_orig_data) > 0:
            self.btn_compare.config(state='active')

    def shot(self):
        self.is_shotting = True
        self.frame_count = 0
        self.OUTDATA = {
            'materialname': '',
            'framenumber': 100,
            'frames': [],
            'means': [],
            'mins': [],
            'maxs': [],
            'ffgz_size': [],
            'start_datetime': None,
            'finish_datetime': None,
            'thresh': None,
            'contrast': None,
            'bright': None
        }
        self.OUTDATA['materialname'] = self.materialname.get()
        self.OUTDATA['framenumber'] = self.framenumber.get()
        self.OUTDATA['thresh'] = self.threshvar.get()
        self.OUTDATA['contrast'] = self.contrastvar.get()
        self.OUTDATA['bright'] = self.brightvar.get()

        try:
            self.init_camera()
            # take 10 images for preparing
            for i in range(10):
                self.camera.get_origin_frames()
            self.update_canvas()
        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}\n")

    def compare(self):
        pass

    def show_opencv_window(self, image):
        cv.namedWindow('OpenCV Window', cv.WINDOW_NORMAL)
        cv.imshow('OpenCV Window', image)

    def hide_opencv_window(self):
        cv.destroyAllWindows()

    def datetimenow(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def write_outdata(self):
        filename = self.OUTDATA['materialname'].replace(' ', '_')
        create_folder(myos.MATERIALSDIR)
        with open(f"{myos.MATERIALSDIR}{filename}.json", 'w') as outfile:
            json.dump(self.OUTDATA, outfile)

    def grab_frame(self, *args, **kwargs):
        '''returns grabbed frame '''
        pass

    def update_canvas(self, *args, **kwargs):
        try:
            self.OUTDATA['start_datetime'] = self.datetimenow()
            image = self.grab_frame()
            if image is not None:
                # convert to RGB image for canvas
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                # scale image by percent
                scaledimage = self.camera.resize_frame(
                    image,
                    scale_percent=self.get_scale_orig()
                )
                self.canvasimage = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(scaledimage)
                )
                self.canvas_image.create_image(
                    0, 0, image=self.canvasimage, anchor=tk.NW
                )
                self.after(self.delay_for_img_canvas, self.update_canvas)
        except Exception as exc:
            self.txt_log.insert('0.0', f"update_canvas(): {exc}\n")
            messagebox.showerror("[Error] ", exc)

    def get_materialname(self, event=None):
        return event.widget.get()

    def get_framenumber(self, event=None):
        return int(event.widget.get())

    def get_threshval(self, event=None):
        val = int(self.scale_thresh.get())
        self.lb_threshval['text'] = str(val)
        return val

    def get_contrastval(self, event=None):
        val = int(self.scale_contrast.get()) / 10
        self.lb_contrastval['text'] = str(val)
        return val

    def get_brightval(self, event=None):
        val = int(self.scale_bright.get())
        self.lb_brightval['text'] = str(val)
        return val

    def get_kernel(self, event=None):
        val = self.combobox_kernel.get()
        return base.KERNELS[val]

    def get_threshtype(self, event=None):
        val = self.combobox_thresh.get()
        return val

    def get_thresholded_image(self, image, *args, **kwargs):
        image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        # Block Size - It decides the size of neighbourhood area.
        # C - It is just a constant which is subtracted from the mean or weighted mean calculated.
        if self.combobox_thresh.get() == 'adaptive_thresh_mean_c':
            image = cv.adaptiveThreshold(
                src=image, maxValue=255,
                adaptiveMethod=cv.ADAPTIVE_THRESH_MEAN_C,
                thresholdType=cv.THRESH_BINARY,
                blockSize=11, C=2
            )
        if self.combobox_thresh.get() == 'adaptive_thresh_gaussian_c':
            image = cv.adaptiveThreshold(
                src=image, maxValue=255,
                adaptiveMethod=cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                thresholdType=cv.THRESH_BINARY,
                blockSize=11, C=2
            )
        if 'ffg_mean' in kwargs:
            ffg_mean = kwargs['ffg_mean']
            if self.combobox_thresh.get() == 'binary':
                ret, image = cv.threshold(
                    src=image, thresh=ffg_mean,
                    maxval=255, type=cv.THRESH_BINARY, dst=None)
            if self.combobox_thresh.get() == 'binary_inv':
                ret, image = cv.threshold(
                    src=image, thresh=ffg_mean,
                    maxval=255, type=cv.THRESH_BINARY_INV)
            if self.combobox_thresh.get() == 'tozero':
                ret, image = cv.threshold(
                    src=image, thresh=ffg_mean,
                    maxval=255, type=cv.THRESH_TOZERO)
            if self.combobox_thresh.get() == 'tozero_inv':
                ret, image = cv.threshold(
                    src=image, thresh=ffg_mean,
                    maxval=255, type=cv.THRESH_TOZERO_INV)
            if self.combobox_thresh.get() == 'trunc':
                ret, image = cv.threshold(
                    src=image, thresh=ffg_mean,
                    maxval=255, type=cv.THRESH_TRUNC)

        return image

    def get_colorspace(self, event=None):
        val = self.combobox_colorspace.get()
        return val

    def get_image_by_colorspace(self, image, *args, **kwargs):
        if self.combobox_colorspace.get() == 'Gray':
            image = self.camera.get_frame_as_gray(image)
        if self.combobox_colorspace.get() == 'HSV':
            image = self.camera.get_frame_as_hsv(image)
        if self.combobox_colorspace.get() == 'CIELab':
            image = self.camera.get_frame_as_lab(image)
        if self.combobox_colorspace.get() == 'YUV':
            image = self.camera.get_frame_as_yuv(image)
        if self.combobox_colorspace.get() == 'YCrCB':
            image = self.camera.get_frame_as_ycrcb(image)

        return image

    def select_morph_opr(self, event=None):
        val = self.combobox_morph_opr.get()
        return val

    def get_image_by_morph_opr(self, image, *args, **kwargs):
        if self.combobox_morph_opr.get() == 'erosion':
            image = self.camera.get_image_erosion(image)
        if self.combobox_morph_opr.get() == 'dilation':
            image = self.camera.get_image_dilation(image)
        if self.combobox_morph_opr.get() == 'opening':
            image = self.camera.get_image_opening(image)
        if self.combobox_morph_opr.get() == 'closing':
            image = self.camera.get_image_closing(image)
        if self.combobox_morph_opr.get() == 'gradient':
            image = self.camera.get_image_morph_gradient(image)
        if self.combobox_morph_opr.get() == 'top hat':
            image = self.camera.get_image_tophat(image)
        if self.combobox_morph_opr.get() == 'black hat':
            image = self.camera.get_image_blackhat(image)

        return image

    def select_image_gradient(self, event=None):
        val = self.combobox_gradient.get()
        return val

    def get_image_by_gradient(self, image):
        if self.combobox_gradient.get() == 'laplacian':
            image = self.camera.get_image_gradient_laplacian(image)
        if self.combobox_gradient.get() == 'sobelx':
            image = self.camera.get_image_gradient_sobelx(image)
        if self.combobox_gradient.get() == 'sobely':
            image = self.camera.get_image_gradient_sobely(image)
        return image

    def animate(self, i):
        selected_tab = self.notebook_footer.tab(
            self.notebook_footer.select(), 'text'
        )
        if selected_tab == 'Live Histogram':
            if self.image is not None:
                try:
                    # self.txt_log.insert('0.0', f"{i} drawing histogram...\n")
                    self.ax.clear()
                    # image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
                    histr = cv.calcHist([self.image], [0],
                                        None, [256], [1, 256])
                    self.ax.plot(histr, color='b')

                    # colors = ('b', 'g', 'r')
                    # for i, color in enumerate(colors):
                    #     histr = cv.calcHist(
                    #         [self.image], [i], None, [256], [1, 256])
                    #     # annot_max(,self.ax)
                    #     self.ax.plot(histr, color=color)

                except Exception as exc:
                    self.txt_log.insert('0.0', f"animate Exception:\n {exc}")

    def ui_compare(self, *args, **kwargs):
        # Figure for plotting
        self.fig_compare = Figure(figsize=(5, 4), dpi=100,
                                  facecolor='#BDBDBD', tight_layout=True)
        self.ax_compare = self.fig_compare.add_subplot(111)
        # A tk.DrawingArea.
        self.figcanvas_compare = FigureCanvasTkAgg(
            self.fig_compare, master=self.frame_plotcompare)
        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(
            self.figcanvas_compare, self.frame_plotcompare, pack_toolbar=False)
        toolbar.update()
        self.figcanvas_compare.mpl_connect(
            "key_press_event",
            lambda event: print(f"you pressed {event.key}")
        )
        self.figcanvas_compare.mpl_connect(
            "key_press_event", key_press_handler)

        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.figcanvas_compare.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def draw_compare_graph(self, original, sample):
        bins = np.linspace(0, 255, 100)
        self.fig_compare.delaxes(self.ax_compare)
        self.ax_compare = self.fig_compare.add_subplot(111)
        self.ax_compare.hist(original, bins, alpha=0.5, label='original')
        self.ax_compare.hist(sample, bins, alpha=0.5, label='sample')
        self.ax_compare.set_xlabel('FFG Mean', fontsize=10)
        self.ax_compare.set_ylabel('Frame Number', fontsize=10)
        self.ax_compare.legend(loc='upper right')
        self.figcanvas_compare.draw()
        self.ax_compare.plot()

    def create_tooltips(self):
        CreateToolTip(self.btn_upload_original, text='Upload Original Image')
        CreateToolTip(self.btn_upload_sample, text='Upload Sample Image')
        CreateToolTip(self.btn_shot, text='Start Shotting')
        CreateToolTip(self.btn_compare, text='Comapre Original and Sample')
