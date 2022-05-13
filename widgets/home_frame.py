import sys
from pathlib import Path
import os
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
from .home_widget import HomeWidget
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


class HomeFrame(HomeWidget):
    def __init__(self, *args, **kwargs):
        HomeWidget.__init__(self, *args, **kwargs)
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
        # Checkbox OpenCV window
        self.cb_opencv_var = tk.BooleanVar(self.frame_cb_opencv)
        self.cb_opencv_window.configure(variable=self.cb_opencv_var)
        # Checkbox Equalization histogram
        self.cb_equalhist_var = tk.BooleanVar(self.frame_equalizationhist)
        self.cb_equal_hist.configure(variable=self.cb_equalhist_var)
        self.cb_histeq_gray_var = tk.BooleanVar(self.frame_equalizationhist)
        self.cb_histeq_gray.configure(variable=self.cb_histeq_gray_var)
        self.cb_histeq_bgr_var = tk.BooleanVar(self.frame_equalizationhist)
        self.cb_histeq_bgr.configure(variable=self.cb_histeq_bgr_var)
        # Checkbox colorspace channels
        self.cb_ch1_var = tk.BooleanVar(self.frame_color_channels)
        self.cb_ch2_var = tk.BooleanVar(self.frame_color_channels)
        self.cb_ch3_var = tk.BooleanVar(self.frame_color_channels)
        self.cb_ch1.configure(variable=self.cb_ch1_var)
        self.cb_ch2.configure(variable=self.cb_ch2_var)
        self.cb_ch3.configure(variable=self.cb_ch3_var)
        # Checkbox CLAHE
        self.cb_clahe_var = tk.BooleanVar(self.frame_clahe)
        self.cb_clahe.configure(variable=self.cb_clahe_var)
        self.cb_clahe_gray_var = tk.BooleanVar(self.frame_clahe)
        self.cb_clahe_gray.configure(variable=self.cb_clahe_gray_var)
        self.cb_clahe_bgr_var = tk.BooleanVar(self.frame_clahe)
        self.cb_clahe_bgr.configure(variable=self.cb_clahe_bgr_var)
        # Checkbox Canny Edge
        self.cb_cannyvar = tk.BooleanVar(self.frame_canny)
        self.cb_canny.configure(variable=self.cb_cannyvar)
        # Checkbox auto brightness contrast
        self.cb_auto_contrast_brightness_var = tk.BooleanVar(
            self.frame_auto_contrast_brightness)
        self.cb_auto_contrast_brightness.configure(
            variable=self.cb_auto_contrast_brightness_var)
        self.cb_adjust_gamma_var = tk.BooleanVar(self.frame_gamma_correction)
        self.cb_adjust_gamma.configure(variable=self.cb_adjust_gamma_var)
        # image Scale init value
        self.scalepercentvar = tk.IntVar(self.frame_scalepercent, value=50)
        self.scale_scalepercent.configure(variable=self.scalepercentvar)
        self.lb_scalevar.configure(text=self.scalepercentvar.get())
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
        self.combobox_colorspace.set(base.COLORSPACES[0])
        # Combobox morphological operation init values
        self.combobox_morph_opr.configure(values=base.MORPHOLOGICAL_OPERATIONS)
        self.combobox_morph_opr.set('None')
        # Combobox blur types init values
        self.combo_blur.configure(values=base.BLUR_TYPES)
        self.combo_blur.set('None')
        self.combobox_sharpen.configure(values=base.SHARPENING_LIST)
        self.combobox_sharpen.set('None')
        self.cb_removenoise_var = tk.BooleanVar(self.frame_removenoise)
        self.cb_removenoise.configure(variable=self.cb_removenoise_var)

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
        self.spinbox_morph_kernelsize.set('5')
        self.spin_cliplimit.set('8')
        self.spin_tilegridsize.set('8')
        self.lb_tilegridsize_res.config(text=f"(8,8)")
        self.sb_canny_min.set('100')
        self.sb_canny_max.set('200')
        style_spin = ttk.Style()
        style_spin.configure("TSpinbox", arrowsize=20, arrowcolor="#336699")
        self.sb_canny_min.config(style='TSpinbox')
        # histogram
        self.ui_histogram()
        # canvas
        self.canvas_image.bind("<Button-1>", self.get_pixel_rgb_value)

    def init_camera(self):
        with open(base.SETTINGS_FILE, 'r') as settingsfile:
            base.SETTINGS = json.load(settingsfile)
        if base.SETTINGS['default_camera'] == 'external':
            from cameras.external import External
            self.camera = External()
        else:
            try:
                cam_source = base.SETTINGS['selected_camera']
                if platform.startswith('linux'):
                    pass
                else:
                    cam_source = int(cam_source)
                self.camera = Webcam(cam_source=cam_source)
            except Exception as exc:
                self.txt_log.insert('0.0', f"{exc}\n")

    def set_frame(self, frame):
        self.frame = frame

    def get_frame(self):
        return self.frame

    def start(self):
        try:
            # self.canvas_image.config(width=self.camera.width)
            # self.canvas_image.config(height=self.camera.height)
            self.init_camera()
            self.is_started = True
            # take 10 images for preparing
            for i in range(10):
                self.camera.get_origin_frames()
            self.update_canvas()
        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}\n")

    def stop(self):
        self.camera.__del__()
        # self.canvas_image.destroy()

    def save(self):
        try:
            if self.is_started:
                outImageName = datetime.datetime.now().strftime("img_%Y_%m_%d_%H_%M_%S")
                create_folder(myos.DATASETDIR)
                outfile = os.path.join(myos.DATASETDIR, f'{outImageName}.jpg')
                cv.imwrite(outfile, self.image)
                self.txt_log.insert('0.0', f"\tThe image is saved!\t")
                # self.stop()
        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}")

    def browse(self):
        file = askopenfile(
            initialdir=base.BASEDIR,
            title="Select a File",
            filetypes=(
                ("all files", "*.*"),
                ("Text files", "*.txt*")
            )
        )

        src = file.name
        image = cv.imread(src)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.init_camera()
        scaledimage = self.camera.resize_frame(
            image,
            scale_percent=self.get_scalevar()
        )
        self.canvasimage = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(scaledimage)
        )
        self.canvas_image.create_image(
            0, 0, image=self.canvasimage, anchor=tk.NW
        )

        # Change label contents
        # label_file_explorer.configure(text="File Opened: "+filename)

    def choose_original_data(self):
        file = askopenfile(
            initialdir=myos.MATERIALSDIR,
            title="Select Original Data File",
            filetypes=(
                ("json files", "*.json*"),
                ("all files", "*.*")
            )
        )
        if file:
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
        # image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
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
                # scale image by percent
                self.resized_img = self.camera.resize_frame(
                    image,
                    scale_percent=self.get_scalevar()
                )
                # TODO: canvas width, height is not equal resied_img. Fix this.
                # h, w, c = self.resized_img.shape
                # self.canvas_image.config(width=w, height=h)
                self.canvasimage = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(self.resized_img)
                )
                self.canvas_image.create_image(
                    0, 0, image=self.canvasimage, anchor=tk.NW
                )
                self.after(self.delay_for_img_canvas, self.update_canvas)
        except Exception as exc:
            self.txt_log.insert('0.0', f"update_canvas(): {exc}\n")
            messagebox.showerror("[Error] ", exc)

    def get_pixel_rgb_value(self, event=None):
        try:
            r, g, b = self.resized_img[event.x, event.y]
            # print(f"RGB: {r}, {g}, {b}")
        except Exception as exc:
            self.txt_log.insert('0.0', f"get_pixel_rgb_value(): {exc}\n")

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

    def get_scalevar(self, event=None):
        val = int(self.scale_scalepercent.get())
        self.lb_scalevar['text'] = str(val)
        return val

    def get_kernel(self, event=None):
        val = self.combobox_kernel.get()
        return base.KERNELS[val]

    def get_threshtype(self, event=None):
        val = self.combobox_thresh.get()
        return val

    def get_thresholded_image(self, image, *args, **kwargs):
        try:
            if len(image.shape) == 3:
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
            if 'threshval' in kwargs:
                threshval = kwargs['threshval']
                if self.combobox_thresh.get() == 'binary':
                    ret, image = cv.threshold(
                        src=image, thresh=threshval,
                        maxval=255, type=cv.THRESH_BINARY, dst=None)
                if self.combobox_thresh.get() == 'binary_inv':
                    ret, image = cv.threshold(
                        src=image, thresh=threshval,
                        maxval=255, type=cv.THRESH_BINARY_INV)
                if self.combobox_thresh.get() == 'tozero':
                    ret, image = cv.threshold(
                        src=image, thresh=threshval,
                        maxval=255, type=cv.THRESH_TOZERO)
                if self.combobox_thresh.get() == 'tozero_inv':
                    ret, image = cv.threshold(
                        src=image, thresh=threshval,
                        maxval=255, type=cv.THRESH_TOZERO_INV)
                if self.combobox_thresh.get() == 'trunc':
                    ret, image = cv.threshold(
                        src=image, thresh=threshval,
                        maxval=255, type=cv.THRESH_TRUNC)

            return image
        except Exception as exc:
            self.txt_log.insert('0.0', f"get_thresholded_image(): {exc}\n")

    def get_colorspace(self, event=None):
        val = self.combobox_colorspace.get()
        return val

    def get_image_by_colorspace(self, image, *args, **kwargs):
        if self.combobox_colorspace.get() == 'RGB':
            image = self.camera.get_frame_as_rgb(image)
        if self.combobox_colorspace.get() == 'Gray':
            image = self.camera.get_frame_as_gray(image)
        if self.combobox_colorspace.get() == 'HSV':
            image = self.camera.get_frame_as_hsv(image)
        if self.combobox_colorspace.get() == 'CIELab':
            image = self.camera.get_frame_as_lab(image)
        if self.combobox_colorspace.get() == 'YUV':
            image = self.camera.get_frame_as_yuv(image)
        if self.combobox_colorspace.get() == 'YCrCb':
            image = self.camera.get_frame_as_ycrcb(image)
        if self.combobox_colorspace.get() == 'Luv':
            image = self.camera.get_frame_as_luv(image)
        if self.combobox_colorspace.get() == 'HLS':
            image = self.camera.get_frame_as_hls(image)

        return image

    def get_equalized_image(self, image):
        try:
            channels = (
                self.cb_ch1_var.get(),
                self.cb_ch2_var.get(),
                self.cb_ch3_var.get()
            )
            if self.get_colorspace() == 'Gray':
                image = self.camera.equalize_gray_frame(image)
                self.txt_log.insert('0.0', f"\tEqualize Gray\t")
            if self.get_colorspace() == 'BGR':
                image = self.camera.equalize_frame(image, channels)
                self.txt_log.insert('0.0', f"\tEqualize BGR\t")
            if self.get_colorspace() == 'CIELab':
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_LAB2BGR)
                self.txt_log.insert('0.0', f"\tEqualize CIELab\t")
            if self.get_colorspace() == 'HSV':
                image = self.camera.equalize_frame(image, channels)
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_HSV2BGR)
                self.txt_log.insert('0.0', f"\tEqualize HSV\t")
            if self.get_colorspace() == 'HLS':
                image = self.camera.equalize_frame(image, channels)
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_HLS2BGR)
                self.txt_log.insert('0.0', f"\tEqualize HLS\t")
            if self.get_colorspace() == 'YUV':
                image = self.camera.equalize_frame(image, channels)
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_YUV2BGR)
                self.txt_log.insert('0.0', f"\tEqualize YUV\t")
            if self.get_colorspace() == 'YCrCb':
                image = self.camera.equalize_frame(image, channels)
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_YCrCb2BGR)
                self.txt_log.insert('0.0', f"\tEqualize YCrCb\t")
            if self.get_colorspace() == 'Luv':
                image = self.camera.equalize_frame(image, channels)
                if self.cb_histeq_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_Luv2BGR)
                self.txt_log.insert('0.0', f"\tEqualize Luv\t")
                image = self.camera.equalize_frame(image, channels)

            if self.get_colorspace() != 'Gray' and self.cb_histeq_bgr_var.get() and self.cb_histeq_gray_var.get():
                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

            return image
        except Exception as exc:
            self.txt_log.insert('0.0', f"get_equalized_image(): {exc}\n")

    def get_clahed_image(self, image, c, t):
        try:
            channels = (
                self.cb_ch1_var.get(),
                self.cb_ch2_var.get(),
                self.cb_ch3_var.get()
            )
            if self.get_colorspace() == 'Gray':
                image = self.camera.clahe_gray_frame(image, c, t)
                self.txt_log.insert('0.0', f"\tClahe Gray\t")
            if self.get_colorspace() == 'BGR':
                image = self.camera.clahe_frame(image, channels, c, t)
                self.txt_log.insert('0.0', f"\tClahe BGR\t")
            if self.get_colorspace() == 'CIELab':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_LAB2BGR)
                self.txt_log.insert('0.0', f"\tClahe CIELab\t")
            if self.get_colorspace() == 'HSV':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_HSV2BGR)
                self.txt_log.insert('0.0', f"\tClahe HSV\t")
            if self.get_colorspace() == 'HLS':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_HLS2BGR)
                self.txt_log.insert('0.0', f"\tClahe HLS\t")
            if self.get_colorspace() == 'YUV':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_YUV2BGR)
                self.txt_log.insert('0.0', f"\tClahe Yuv\t")
            if self.get_colorspace() == 'YCrCb':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_YCR_CB2BGR)
                self.txt_log.insert('0.0', f"\tClahe YCrCb\t")
            if self.get_colorspace() == 'Luv':
                image = self.camera.clahe_frame(image, channels, c, t)
                if self.cb_clahe_bgr_var.get():
                    image = cv.cvtColor(image, cv.COLOR_Luv2BGR)
                self.txt_log.insert('0.0', f"\tClahe Luv\t")

            if self.get_colorspace() != 'Gray' and self.cb_clahe_bgr_var.get() and self.cb_clahe_gray_var.get():
                image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            return image
        except Exception as exc:
            self.txt_log.insert('0.0', f"get_clahed_image(): {exc}\n")

    def gamma_adjusting(self, image, gamma_val):

        if self.get_colorspace() == 'Gray':
            image = self.camera.adjust_gamma_grayframe(
                image, gamma_val)

        if self.get_colorspace() == 'HSV':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_HSV2BGR)

        if self.get_colorspace() == 'YUV':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_YUV2BGR)

        if self.get_colorspace() == 'YCrCb':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_YCR_CB2BGR)

        if self.get_colorspace() == 'Luv':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_Luv2BGR)

        if self.get_colorspace() == 'CIELab':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_LAB2BGR)

        if self.get_colorspace() == 'HLS':
            image = self.camera.adjust_gamma(
                image,  gamma_val)
            image = cv.cvtColor(image, cv.COLOR_HLS2BGR)

        if self.get_colorspace() == 'BGR':
            image = self.camera.adjust_gamma(
                image,  gamma_val)

        return image

    def get_canny_image(self, image):
        min = int(self.sb_canny_min.get())
        max = int(self.sb_canny_max.get())
        if max > min:
            image = self.camera.apply_image_canny_edge(
                image, min, max)
        else:
            messagebox.showerror(
                "[Error] ",
                "Canny Edge max value must be greater than min value"
            )
            self.sb_canny_max.set(f"{str(max+1)}")
        return image

    def select_morph_opr(self, event=None):
        val = self.combobox_morph_opr.get()
        return val

    def select_blur_type(self, event=None):
        val = self.combo_blur.get()
        return val

    def select_sharping(self, event=None):
        val = self.combobox_sharpen.get()
        return val

    def get_image_by_morph_opr(self, image, ks, *args, **kwargs):
        if self.combobox_morph_opr.get() == 'erosion':
            image = self.camera.get_image_erosion(image, ks)
        if self.combobox_morph_opr.get() == 'dilation':
            image = self.camera.get_image_dilation(image, ks)
        if self.combobox_morph_opr.get() == 'opening':
            image = self.camera.get_image_opening(image, ks)
        if self.combobox_morph_opr.get() == 'closing':
            image = self.camera.get_image_closing(image, ks)
        if self.combobox_morph_opr.get() == 'gradient':
            image = self.camera.get_image_morph_gradient(image, ks)
        if self.combobox_morph_opr.get() == 'top hat':
            image = self.camera.get_image_tophat(image, ks)
        if self.combobox_morph_opr.get() == 'black hat':
            image = self.camera.get_image_blackhat(image, ks)

        return image

    def sharpen_image_by_selected(self, image):
        if self.combobox_sharpen.get() == "sharpen1":
            image = self.camera.sharpen_frame_1(image)
        if self.combobox_sharpen.get() == "sharpen2":
            image = self.camera.sharpen_frame_2(image)
        if self.combobox_sharpen.get() == "sharpen3":
            image = self.camera.sharpen_frame_3(image)
        if self.combobox_sharpen.get() == "sharpen4":
            image = self.camera.sharpen_frame_4(image)
        return image

    def blur_image_by_selected(self, image):
        try:
            ksize = int(self.spinbox_blur_kernel.get())
            if self.combo_blur.get() == 'blur':
                image = cv.blur(image, ksize=(ksize, ksize))
            if self.combo_blur.get() == 'median':
                image = cv.medianBlur(image, ksize)
            if self.combo_blur.get() == 'gaussian':
                image = cv.GaussianBlur(image, ksize=(
                    ksize, ksize), sigmaX=0,
                    dst=None, sigmaY=None, borderType=None)

            return image
        except Exception as exc:
            self.txt_log.insert('0.0', f"blur_image_by_selected(): {exc}\n")

    def show_current_img_histogram(self):
        try:
            ffgz = self.image[self.image > 0]
            # ffgz = np.sort(ffgz)
            fig = plt.figure(
                figsize=(5, 4), dpi=100,
                facecolor='#BDBDBD',
                tight_layout=True
            )
            ax = fig.add_subplot(111)
            # bins = np.linspace(0, 255, 100)
            histr = cv.calcHist([ffgz], [0], None, [256], [0, 256])
            ax.plot(histr, color='b', label=f'Hist', alpha=0.5)
            ax.set_xlabel(
                f'RGB Values\nFrequent Value is {np.bincount(ffgz).argmax()}', fontsize=10)
            ax.set_ylabel('Pixel Amount', fontsize=10)
            ax.legend(loc='upper right')
            self.stop()
            plt.show()
        except Exception as exc:
            self.txt_log.insert(
                '0.0', f"show_current_img_histogram(): {exc}\n")

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

    def ui_histogram(self, *args, **kwargs):
        # Figure for plotting
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        # A tk.DrawingArea.
        canvas = FigureCanvasTkAgg(self.fig, master=self.frame_livehistogram)
        canvas.draw()
        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(
            canvas, self.frame_livehistogram, pack_toolbar=False)
        toolbar.update()
        canvas.mpl_connect(
            "key_press_event",
            lambda event: print(f"you pressed {event.key}")
        )
        canvas.mpl_connect("key_press_event", key_press_handler)

        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

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
        CreateToolTip(self.btn_start, text='Start Camera')
        CreateToolTip(self.btn_stop, text='Stop Camera')
        CreateToolTip(self.btn_shot, text='Start Shotting')
        CreateToolTip(self.btn_browse, text='Browse File')
        CreateToolTip(self.btn_save, text='Save The Image')
        CreateToolTip(self.btn_compare, text='Comapre Original and Sample')
