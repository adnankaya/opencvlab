import json
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import PIL.Image
import PIL.ImageTk
import cv2 as cv
import numpy as np
import datetime
import time
import matplotlib.animation as animation
# internals
from widgets.home_frame import HomeFrame
from widgets.lab_frame import LabFrame
from widgets.settings_frame import SettingsFrame
from cameras.webcam import Webcam
from settings import base
from settings import windows as win


with open(base.SETTINGS_FILE, 'r') as settingsfile:
    base.SETTINGS = json.load(settingsfile)


class Home(HomeFrame):
    def __init__(self, *args, **kwargs):
        HomeFrame.__init__(self, *args, **kwargs)

    def grab_frame(self, *args, **kwargs):
        try:
            cpu_start_time = time.process_time()
            start_time = time.time()
            self.image = self.camera.get_origin_frames()
            if self.image is not None:
                h, w, c = self.image.shape
                self.lb_shapeval.config(text=f"{w}x{h}")
                if self.cb_orig_adjusted_var.get():
                    self.cb_orig_or_adjusted.config(text='Adjusted')
                    if self.cb_threshvar.get():
                        self.image = self.camera.get_frame_foreground(
                            self.image,
                            threshval=self.get_threshval(),
                            kernel=self.get_kernel()
                        )
                        self.txt_log.insert('0.0', f"\t[1.]Frame Foreground\t")
            
                    if self.cb_conrastvar.get() and self.cb_brightvar.get():
                        self.image = self.camera.get_contrasted_frame(
                            self.image,
                            alpha=self.get_contrastval(),
                            beta=self.get_brightval()
                        )
                    if self.cb_auto_contrast_brightness_var.get():
                        self.image = self.camera.apply_auto_contrast_bright(
                            self.image)
                    if self.cb_removenoise_var.get():
                        self.image = self.camera.remove_noises(
                            self.image)

                    if self.get_colorspace() != 'None':
                        self.image = self.get_image_by_colorspace(
                            self.image
                        )

                    if self.select_morph_opr() != 'None':
                        kernelsize = int(
                            self.spinbox_morph_kernelsize.get())
                        self.image = self.get_image_by_morph_opr(
                            self.image, (kernelsize, kernelsize)
                        )

                    if self.select_blur_type() != 'None':
                        self.image = self.blur_image_by_selected(
                            self.image)

                    if self.select_sharping() != 'None':
                        self.image = self.sharpen_image_by_selected(
                            self.image)

                    if self.cb_equalhist_var.get():
                        self.image = self.get_equalized_image(self.image)
                        if not self.cb_histeq_gray_var.get():
                            self.image = self.camera.get_frame_foreground(
                                self.image)

                    if self.cb_clahe_var.get():
                        cliplimit = float(self.spin_cliplimit.get())
                        tilegridsize = int(self.spin_tilegridsize.get())
                        tilegridsize = (tilegridsize, tilegridsize)
                        self.lb_tilegridsize_res.config(
                            text=f"{str(tilegridsize)}"
                        )
                        self.image = self.get_clahed_image(
                            self.image, cliplimit, tilegridsize
                        )

                    if self.cb_adjust_gamma_var.get():
                        gamma_val = float(self.spinbox_gamma.get())
                        self.image = self.gamma_adjusting(
                            self.image, gamma_val)

                    if self.cb_cannyvar.get():
                        self.image = self.get_canny_image(self.image)

                    if self.get_threshtype() != 'None':
                        threshval = float(self.spinbox_thresh_val.get())
                        self.image = self.get_thresholded_image(
                            self.image, threshval=threshval
                        )
                    ffg_mean = self.camera.get_frame_foreground_mean(
                        self.image)
                    if ffg_mean > 0:
                        self.frame_count += 1
                        # TODO move to elsewhere
                        fsize, fmin, fmax = self.camera.get_ffgz_size_min_max(
                            self.image)
                        self.lb_framenumberval.config(
                            text=self.frame_count)
                        self.lb_meanval.config(text=ffg_mean)
                        self.lb_minval.config(text=fmin)
                        self.lb_maxval.config(text=fmax)
                        self.lb_ffgzval.config(text=fsize)
                        ffgz = self.image[self.image > 0]
                        freq_val = np.bincount(ffgz).argmax()
                        self.txt_log.insert(
                            '0.0',
                            f"\tFFG-> Freq Val: {freq_val}\n"
                        )
                        if self.is_shotting:
                            self.OUTDATA['frames'].append(self.frame_count)
                            self.OUTDATA['means'].append(ffg_mean)
                            self.OUTDATA['mins'].append(float(fmin))
                            self.OUTDATA['maxs'].append(float(fmax))
                            self.OUTDATA['ffgz_size'].append(fsize)

                            if self.frame_count == self.framenumber.get():
                                self.stop()
                                self.is_shotting = False
                                self.OUTDATA['finish_datetime'] = self.datetimenow(
                                )
                                self.text_outdata.insert(
                                    '0.0', f"Outdata: \n")
                                self.text_outdata.insert(
                                    '20.10', f"{self.OUTDATA}")
                                self.write_outdata()
                                self.frame_count = 0
                                return
                        if self.is_comparing:
                            self.img_sample_data['means'].append(ffg_mean)
                            if self.frame_count == self.img_orig_data['framenumber']:
                                self.stop()
                                self.is_comparing = False
                                self.frame_count = 0
                                original = self.img_orig_data['means']
                                sample = self.img_sample_data['means']
                                # draw comparing graph
                                self.draw_compare_graph(original, sample)
                                return

                        cpu_end_time = time.process_time()
                        end_time = time.time()
                        cpu_duration = format(
                            round(cpu_end_time-cpu_start_time, 4), '.4f')
                        duration = format(
                            round(end_time-start_time, 4), '.4f')
                        self.lb_cpu_dur_val.config(
                            text=f"{cpu_duration}"
                        )
                        self.lb_duration_val.config(
                            text=f"{duration}"
                        )
            
                else:
                    self.cb_orig_or_adjusted.config(text='Original')

                if self.cb_opencv_var.get():
                    self.show_opencv_window(self.image)
                else:
                    self.hide_opencv_window()
                return self.image
        except Exception as exc:
            self.txt_log.insert('0.0', f"grab_frame(): {exc}\n")
            messagebox.showerror("[Error] ", exc)

    def compare(self):
        self.is_comparing = True
        self.frame_count = 0
        self.img_sample_data = {'means': []}
        try:
            self.init_camera()
            # take 10 images for preparing
            for i in range(10):
                self.camera.get_origin_frames()
            self.update_canvas()
        except Exception as exc:
            self.txt_log.insert('0.0', f"{exc}\n")


class Main():
    def __init__(self, window, *args, **kwargs):
        self.window = window

        notebook = ttk.Notebook(self.window)

        self.home = Home(notebook)
        self.frame_lab = LabFrame(notebook)
        self.frame_settings = SettingsFrame(notebook)

        notebook.add(self.home, text="Home")
        notebook.add(self.frame_lab, text="|   Lab   |")
        notebook.add(self.frame_settings, text="Settings")

        notebook.pack(expand=True, fill="both")
        # Histogram animation
        ani = animation.FuncAnimation(
            self.home.fig,
            self.home.animate,
            # fargs=(self.home.image,),
            interval=100,
            # blit=True
        )
        self.window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Computer Vision Tool by adnankaya")
    # root.geometry("1300x1000")
    root.geometry("1920x1000")
    Main(root)
