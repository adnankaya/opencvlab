import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrolledframe import ScrolledFrame


class HomeWidget(ttk.Panedwindow):
    def __init__(self, master=None, **kw):
        super(HomeWidget, self).__init__(master, **kw)
        self.frame_buttons = ttk.Frame(self)
        self.frame_btnsave = ttk.Frame(self.frame_buttons)
        self.btn_save = tk.Button(self.frame_btnsave)
        self.btn_save.configure(
            activebackground="#2c2c2c",
            activeforeground="#dedede",
            background="#2c2c2c",
            borderwidth="0",
        )
        self.btn_save.configure(
            cursor="hand2", font="{Verdana} 10 {}", foreground="#dedede", text="Save"
        )
        self.btn_save.pack(anchor="center", side="left")
        self.btn_save.configure(command=self.save)
        self.frame_btnsave.configure(padding="2", relief="flat", width="200")
        self.frame_btnsave.pack(anchor="w", side="left")
        self.frame_btnbrowse = ttk.Frame(self.frame_buttons)
        self.btn_browse = tk.Button(self.frame_btnbrowse)
        self.btn_browse.configure(
            activebackground="#2c2c2c",
            activeforeground="#dedede",
            background="#2c2c2c",
            borderwidth="0",
        )
        self.btn_browse.configure(
            cursor="hand2", font="{Verdana} 10 {}", foreground="#dedede", text="Browse"
        )
        self.btn_browse.pack(anchor="center", side="left")
        self.btn_browse.configure(command=self.browse)
        self.frame_btnbrowse.configure(padding="2", relief="flat", width="200")
        self.frame_btnbrowse.pack(anchor="w", side="left")
        self.frame_cb_opencv = ttk.Frame(self.frame_buttons)
        self.cb_opencv_window = tk.Checkbutton(self.frame_cb_opencv)
        self.cb_opencv_window.configure(cursor="hand2", text="OpenCV Window")
        self.cb_opencv_window.pack(side="top")
        self.frame_cb_opencv.configure(padding="2", relief="flat", width="200")
        self.frame_cb_opencv.pack(padx="5", side="left")
        self.frame_scalepercent = ttk.Frame(self.frame_buttons)
        self.lb_scalepercent = ttk.Label(self.frame_scalepercent)
        self.lb_scalepercent.configure(text="Scale %")
        self.lb_scalepercent.pack(side="left")
        self.lb_scalevar = ttk.Label(self.frame_scalepercent)
        self.lb_scalevar.configure(font="{Arial} 10 {bold}", text="50")
        self.lb_scalevar.pack(side="left")
        self.scale_scalepercent = ttk.Scale(self.frame_scalepercent)
        self.scale_scalepercent.configure(
            cursor="hand2", from_="40", orient="horizontal", to="100"
        )
        self.scale_scalepercent.configure(value="40")
        self.scale_scalepercent.pack(padx="5", pady="5", side="right")
        self.scale_scalepercent.bind("<B1-Motion>", self.get_scalevar, add="")
        self.frame_scalepercent.configure(padding="2", relief="groove", width="200")
        self.frame_scalepercent.pack(expand="false", side="left")
        self.frame_duration_info = ttk.Frame(self.frame_buttons)
        self.frame_cpu_duration = ttk.Frame(self.frame_duration_info)
        self.lb_cpu_dur = ttk.Label(self.frame_cpu_duration)
        self.lb_cpu_dur.configure(font="{arial} 10 {bold}", text="CPU Duration:")
        self.lb_cpu_dur.pack(anchor="w", side="left")
        self.lb_cpu_dur_val = ttk.Label(self.frame_cpu_duration)
        self.lb_cpu_dur_val.configure(
            background="#ffffff", font="{arial} 10 {}", text="0"
        )
        self.lb_cpu_dur_val.pack(side="right")
        self.frame_cpu_duration.configure(height="200", width="200")
        self.frame_cpu_duration.pack(fill="x", side="top")
        self.frame_duration = ttk.Frame(self.frame_duration_info)
        self.lb_duration = ttk.Label(self.frame_duration)
        self.lb_duration.configure(
            font="{arial} 10 {bold}", text="Processing Duration:"
        )
        self.lb_duration.pack(anchor="w", side="left")
        self.lb_duration_val = ttk.Label(self.frame_duration)
        self.lb_duration_val.configure(
            background="#ffffff", font="{arial} 10 {}", text="0"
        )
        self.lb_duration_val.pack(side="right")
        self.frame_duration.configure(height="200", width="200")
        self.frame_duration.pack(anchor="w", fill="x", side="bottom")
        self.frame_duration_info.configure(height="200", width="200")
        self.frame_duration_info.pack(padx="10", side="left")
        self.frame_btnstart = ttk.Frame(self.frame_buttons)
        self.btn_start = tk.Button(self.frame_btnstart)
        self.btn_start.configure(
            activebackground="#01579B",
            activeforeground="#ffffff",
            background="#01579B",
            borderwidth="0",
        )
        self.btn_start.configure(
            cursor="hand2", font="{verdana} 10 {bold}", foreground="#ffffff", padx="5"
        )
        self.btn_start.configure(text="Start")
        self.btn_start.pack(side="top")
        self.btn_start.configure(command=self.start)
        self.frame_btnstart.configure(padding="2", width="200")
        self.frame_btnstart.pack(side="left")
        self.frame_btnstop = ttk.Frame(self.frame_buttons)
        self.btn_stop = tk.Button(self.frame_btnstop)
        self.btn_stop.configure(
            activebackground="#e1031e",
            activeforeground="#ffffff",
            background="#e1031e",
            borderwidth="0",
        )
        self.btn_stop.configure(
            cursor="hand2",
            font="{Verdana} 10 {bold}",
            foreground="#ffffff",
            text="Stop",
        )
        self.btn_stop.pack(anchor="center", padx="5", side="right")
        self.btn_stop.configure(command=self.stop)
        self.frame_btnstop.configure(padding="2", relief="flat", width="200")
        self.frame_btnstop.pack(side="left")
        self.frame_current_img_hist = ttk.Frame(self.frame_buttons)
        self.btn_current_hist = tk.Button(self.frame_current_img_hist)
        self.btn_current_hist.configure(
            activebackground="#2c2c2c",
            activeforeground="#dedede",
            background="#2c2c2c",
            borderwidth="0",
        )
        self.btn_current_hist.configure(
            cursor="hand2",
            font="{verdana} 10 {}",
            foreground="#dedede",
            text="Histogram",
        )
        self.btn_current_hist.pack(side="top")
        self.btn_current_hist.configure(command=self.show_current_img_histogram)
        self.frame_current_img_hist.configure(height="200", width="200")
        self.frame_current_img_hist.pack(padx="10", side="left")
        self.frame_buttons.configure(borderwidth="2", height="200", relief="groove")
        self.frame_buttons.pack(expand="false", side="top")
        self.add(self.frame_buttons, weight="1")
        self.frame_body = ttk.Frame(self)
        self.panedwindow_body = ttk.Panedwindow(self.frame_body, orient="horizontal")
        self.notebook_frame_left = ttk.Notebook(self.panedwindow_body)
        self.scrolledframe_nb_imgprocessing = ScrolledFrame(
            self.notebook_frame_left, scrolltype="both"
        )
        self.frame_orig_or_adjusted = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.cb_orig_or_adjusted = tk.Checkbutton(self.frame_orig_or_adjusted)
        self.cb_orig_or_adjusted.configure(
            cursor="hand2", font="{Courier} 14 {bold}", text="Original"
        )
        self.cb_orig_or_adjusted.pack(side="left")
        self.frame_orig_or_adjusted.configure(padding="2", width="200")
        self.frame_orig_or_adjusted.pack(fill="x", padx="5", pady="2", side="top")
        self.frame_thresh = ttk.Frame(self.scrolledframe_nb_imgprocessing.innerframe)
        self.cb_tresh = tk.Checkbutton(self.frame_thresh)
        self.cb_tresh.configure(
            cursor="hand2", font="{verdana} 10 {bold}", text="Threshold"
        )
        self.cb_tresh.pack(padx="2", pady="2", side="left")
        self.lb_threshval = ttk.Label(self.frame_thresh)
        self.lb_threshval.configure(text="10")
        self.lb_threshval.pack(pady="1", side="left")
        self.scale_thresh = ttk.Scale(self.frame_thresh)
        self.scale_thresh.configure(
            cursor="hand2", from_="0", length="160", orient="horizontal"
        )
        self.scale_thresh.configure(to="255")
        self.scale_thresh.pack(expand="false", pady="2", side="left")
        self.scale_thresh.bind("<B1-Motion>", self.get_threshval, add="")
        self.lb_kernel = ttk.Label(self.frame_thresh)
        self.lb_kernel.configure(text="Kernel")
        self.lb_kernel.pack(padx="5", pady="2", side="left")
        self.combobox_kernel = ttk.Combobox(self.frame_thresh)
        self.combobox_kernel.configure(cursor="hand2", state="readonly", width="6")
        self.combobox_kernel.pack(expand="false", padx="5", pady="2", side="left")
        self.combobox_kernel.bind("<<ComboboxSelected>>", self.get_kernel, add="")
        self.frame_thresh.configure(height="200", relief="groove", width="200")
        self.frame_thresh.pack(expand="false", fill="x", padx="5", pady="5", side="top")
        self.frame_auto_contrast_brightness = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.cb_auto_contrast_brightness = tk.Checkbutton(
            self.frame_auto_contrast_brightness
        )
        self.cb_auto_contrast_brightness.configure(
            cursor="hand2",
            font="{verdana} 10 {bold}",
            text="Auto Contrast & Brightness",
        )
        self.cb_auto_contrast_brightness.pack(padx="2", pady="2", side="left")
        self.frame_auto_contrast_brightness.configure(height="200", width="200")
        self.frame_auto_contrast_brightness.pack(
            fill="x", padx="5", pady="2", side="top"
        )
        self.frame_removenoise = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.cb_removenoise = tk.Checkbutton(self.frame_removenoise)
        self.cb_removenoise.configure(
            cursor="hand2", font="{verdana} 10 {bold}", text="Remove Noise"
        )
        self.cb_removenoise.pack(padx="2", pady="2", side="left")
        self.frame_removenoise.configure(height="200", relief="groove", width="200")
        self.frame_removenoise.pack(fill="x", padx="5", pady="2", side="top")
        self.frame_contrast = ttk.Frame(self.scrolledframe_nb_imgprocessing.innerframe)
        self.cb_contrast = tk.Checkbutton(self.frame_contrast)
        self.cb_contrast.configure(cursor="hand2", text="Contrast")
        self.cb_contrast.pack(expand="false", side="left")
        self.lb_contrastval = ttk.Label(self.frame_contrast)
        self.lb_contrastval.configure(text="1.0")
        self.lb_contrastval.pack(side="left")
        self.scale_contrast = ttk.Scale(self.frame_contrast)
        self.scale_contrast.configure(
            cursor="hand2", from_="1", length="160", orient="horizontal"
        )
        self.scale_contrast.configure(to="30")
        self.scale_contrast.pack(expand="false", padx="5", side="left")
        self.scale_contrast.bind("<B1-Motion>", self.get_contrastval, add="")
        self.frame_contrast.configure(height="200", padding="2", width="200")
        self.frame_contrast.pack(
            anchor="nw", expand="false", fill="x", padx="5", side="top"
        )
        self.frame_brightness = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.cb_bright = tk.Checkbutton(self.frame_brightness)
        self.cb_bright.configure(cursor="hand2", text="Brightness")
        self.cb_bright.pack(side="left")
        self.lb_brightval = ttk.Label(self.frame_brightness)
        self.lb_brightval.configure(text="0")
        self.lb_brightval.pack(side="left")
        self.scale_bright = ttk.Scale(self.frame_brightness)
        self.scale_bright.configure(
            cursor="hand2", from_="-126", length="160", orient="horizontal"
        )
        self.scale_bright.configure(to="126")
        self.scale_bright.pack(expand="false", padx="5", side="left")
        self.scale_bright.bind("<B1-Motion>", self.get_brightval, add="")
        self.frame_brightness.configure(height="200", padding="2", width="200")
        self.frame_brightness.pack(
            anchor="nw", expand="false", fill="x", padx="5", pady="2", side="top"
        )
        self.frame_colorspace = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.frame_colorspace_combo = ttk.Frame(self.frame_colorspace)
        self.lb_colorspace = ttk.Label(self.frame_colorspace_combo)
        self.lb_colorspace.configure(font="{verdana} 10 {bold}", text="Colorspace")
        self.lb_colorspace.pack(anchor="sw", padx="5", pady="5", side="left")
        self.combobox_colorspace = ttk.Combobox(self.frame_colorspace_combo)
        self.combobox_colorspace.configure(state="readonly", width="10")
        self.combobox_colorspace.pack(anchor="nw", padx="5", pady="5", side="left")
        self.combobox_colorspace.bind(
            "<<ComboboxSelected>>", self.get_colorspace, add=""
        )
        self.frame_colorspace_combo.configure(height="200", width="200")
        self.frame_colorspace_combo.pack(fill="x", padx="2", pady="2", side="left")
        self.frame_color_channels = ttk.Frame(self.frame_colorspace)
        self.cb_ch1 = tk.Checkbutton(self.frame_color_channels)
        self.cb_ch1.configure(cursor="hand2", text="Ch1")
        self.cb_ch1.pack(side="left")
        self.cb_ch2 = tk.Checkbutton(self.frame_color_channels)
        self.cb_ch2.configure(cursor="hand2", text="Ch2")
        self.cb_ch2.pack(side="left")
        self.cb_ch3 = tk.Checkbutton(self.frame_color_channels)
        self.cb_ch3.configure(cursor="hand2", text="Ch3")
        self.cb_ch3.pack(side="left")
        self.frame_color_channels.configure(height="200", width="200")
        self.frame_color_channels.pack(padx="2", pady="2", side="left")
        self.frame_colorspace.configure(height="200", relief="groove", width="200")
        self.frame_colorspace.pack(fill="x", padx="5", pady="2", side="top")
        self.frame_morph_transf = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.frame_cb_morph = ttk.Frame(self.frame_morph_transf)
        self.label_morph_opr = ttk.Label(self.frame_cb_morph)
        self.label_morph_opr.configure(font="{verdana} 10 {}", text="Morphology")
        self.label_morph_opr.pack(padx="5", pady="5", side="left")
        self.combobox_morph_opr = ttk.Combobox(self.frame_cb_morph)
        self.combobox_morph_opr.configure(cursor="hand2", state="readonly", width="10")
        self.combobox_morph_opr.pack(padx="5", pady="5", side="left")
        self.combobox_morph_opr.bind(
            "<<ComboboxSelected>>", self.select_morph_opr, add=""
        )
        self.frame_cb_morph.configure(height="200", width="200")
        self.frame_cb_morph.pack(padx="3", pady="3", side="left")
        self.frame_spin_kernelsize = ttk.Frame(self.frame_morph_transf)
        self.lb_morph_kernelsize = ttk.Label(self.frame_spin_kernelsize)
        self.lb_morph_kernelsize.configure(font="{verdana} 10 {}", text="Kernel")
        self.lb_morph_kernelsize.pack(padx="5", pady="5", side="left")
        self.spinbox_morph_kernelsize = ttk.Spinbox(self.frame_spin_kernelsize)
        self.spinbox_morph_kernelsize.configure(
            cursor="hand2", from_="1", to="100", width="6"
        )
        _text_ = """5"""
        self.spinbox_morph_kernelsize.delete("0", "end")
        self.spinbox_morph_kernelsize.insert("0", _text_)
        self.spinbox_morph_kernelsize.pack(padx="5", pady="5", side="left")
        self.frame_spin_kernelsize.configure(height="200", width="200")
        self.frame_spin_kernelsize.pack(padx="3", pady="3", side="left")
        self.frame_morph_transf.configure(height="200", relief="groove", width="200")
        self.frame_morph_transf.pack(
            expand="false", fill="x", padx="5", pady="2", side="top"
        )
        self.frame_blurs = ttk.Frame(self.scrolledframe_nb_imgprocessing.innerframe)
        self.lb_blur_type = ttk.Label(self.frame_blurs)
        self.lb_blur_type.configure(font="{verdana} 10 {bold}", text="Blur Type")
        self.lb_blur_type.pack(padx="3", pady="3", side="left")
        self.combo_blur = ttk.Combobox(self.frame_blurs)
        self.combo_blur.configure(cursor="hand2", state="readonly", width="10")
        self.combo_blur.pack(padx="3", pady="3", side="left")
        self.combo_blur.bind("<<ComboboxSelected>>", self.select_blur_type, add="")
        self.lb_blur_kernel = ttk.Label(self.frame_blurs)
        self.lb_blur_kernel.configure(text="Kernel")
        self.lb_blur_kernel.pack(padx="3", pady="3", side="left")
        self.spinbox_blur_kernel = ttk.Spinbox(self.frame_blurs)
        self.spinbox_blur_kernel.configure(
            cursor="hand2", from_="1", increment="2", to="31"
        )
        self.spinbox_blur_kernel.configure(width="6")
        _text_ = """7"""
        self.spinbox_blur_kernel.delete("0", "end")
        self.spinbox_blur_kernel.insert("0", _text_)
        self.spinbox_blur_kernel.pack(padx="3", pady="3", side="left")
        self.frame_blurs.configure(height="200", relief="groove", width="200")
        self.frame_blurs.pack(fill="x", padx="5", pady="5", side="top")
        self.frame_cb_sharpen = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.lb_sharpen = ttk.Label(self.frame_cb_sharpen)
        self.lb_sharpen.configure(font="{verdana} 10 {bold}", text="Sharpen")
        self.lb_sharpen.pack(padx="5", pady="5", side="left")
        self.combobox_sharpen = ttk.Combobox(self.frame_cb_sharpen)
        self.combobox_sharpen.configure(cursor="hand2", state="readonly", width="10")
        self.combobox_sharpen.pack(padx="5", pady="5", side="left")
        self.combobox_sharpen.bind("<<ComboboxSelected>>", self.select_sharping, add="")
        self.frame_cb_sharpen.configure(height="200", relief="groove", width="200")
        self.frame_cb_sharpen.pack(fill="x", padx="5", side="top")
        self.frame_clahe = ttk.Frame(self.scrolledframe_nb_imgprocessing.innerframe)
        self.cb_clahe = tk.Checkbutton(self.frame_clahe)
        self.cb_clahe.configure(
            cursor="hand2", font="{verdana} 10 {bold}", text="Clahe"
        )
        self.cb_clahe.grid(padx="2", pady="2", sticky="w")
        self.lb_cliplimit = ttk.Label(self.frame_clahe)
        self.lb_cliplimit.configure(font="{verdana} 10 {}", text="ClipLimit")
        self.lb_cliplimit.grid(column="0", padx="2", pady="2", row="1", sticky="w")
        self.spin_cliplimit = ttk.Spinbox(self.frame_clahe)
        self.spin_cliplimit.configure(
            font="{verdana} 10 {}", from_="1", to="256", width="6"
        )
        _text_ = """1"""
        self.spin_cliplimit.delete("0", "end")
        self.spin_cliplimit.insert("0", _text_)
        self.spin_cliplimit.grid(column="1", padx="5", pady="2", row="1", sticky="w")
        self.lb_tilegridsize = ttk.Label(self.frame_clahe)
        self.lb_tilegridsize.configure(font="{verdana} 10 {}", text="Tile Grid Size")
        self.lb_tilegridsize.grid(column="2", padx="5", pady="10", row="1", sticky="w")
        self.spin_tilegridsize = ttk.Spinbox(self.frame_clahe)
        self.spin_tilegridsize.configure(
            cursor="hand2", font="{verdana} 10 {}", from_="1", to="256"
        )
        self.spin_tilegridsize.configure(width="6")
        _text_ = """1"""
        self.spin_tilegridsize.delete("0", "end")
        self.spin_tilegridsize.insert("0", _text_)
        self.spin_tilegridsize.grid(
            column="3", padx="2", pady="10", row="1", sticky="w"
        )
        self.lb_tilegridsize_res = ttk.Label(self.frame_clahe)
        self.lb_tilegridsize_res.configure(font="{Verdana} 10 {bold}", text="(1,1)")
        self.lb_tilegridsize_res.grid(
            column="4", padx="2", pady="10", row="1", sticky="w"
        )
        self.cb_clahe_gray = tk.Checkbutton(self.frame_clahe)
        self.cb_clahe_gray.configure(
            cursor="hand2", font="{verdana} 10 {}", text="Gray"
        )
        self.cb_clahe_gray.grid(column="2", padx="2", pady="2", row="0", sticky="e")
        self.cb_clahe_bgr = tk.Checkbutton(self.frame_clahe)
        self.cb_clahe_bgr.configure(cursor="hand2", text="BGR")
        self.cb_clahe_bgr.grid(column="3", row="0", sticky="e")
        self.frame_clahe.configure(height="200", relief="groove", width="200")
        self.frame_clahe.pack(expand="false", fill="x", padx="5", pady="5", side="top")
        self.frame_combothresh = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.lb_combothresh = ttk.Label(self.frame_combothresh)
        self.lb_combothresh.configure(font="{Georgia} 10 {bold}", text="Thresh Type")
        self.lb_combothresh.pack(padx="5", pady="5", side="left")
        self.combobox_thresh = ttk.Combobox(self.frame_combothresh)
        self.combobox_thresh.configure(cursor="hand2", state="readonly")
        self.combobox_thresh.pack(padx="5", pady="5", side="left")
        self.combobox_thresh.bind("<<ComboboxSelected>>", self.get_threshtype, add="")
        self.lb_thresh_type = ttk.Label(self.frame_combothresh)
        self.lb_thresh_type.configure(font="{verdana} 10 {bold}", text="Val")
        self.lb_thresh_type.pack(padx="2", pady="5", side="left")
        self.spinbox_thresh_val = ttk.Spinbox(self.frame_combothresh)
        self.spinbox_thresh_val.configure(from_="0", to="255")
        _text_ = """0"""
        self.spinbox_thresh_val.delete("0", "end")
        self.spinbox_thresh_val.insert("0", _text_)
        self.spinbox_thresh_val.pack(padx="5", pady="5", side="left")
        self.frame_combothresh.configure(height="200", relief="groove", width="200")
        self.frame_combothresh.pack(
            expand="false", fill="x", padx="5", pady="5", side="top"
        )
        self.frame_equalizationhist = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.cb_equal_hist = tk.Checkbutton(self.frame_equalizationhist)
        self.cb_equal_hist.configure(
            cursor="hand2", font="{Verdana} 10 {}", text="Equalize"
        )
        self.cb_equal_hist.pack(padx="2", pady="2", side="left")
        self.cb_histeq_gray = tk.Checkbutton(self.frame_equalizationhist)
        self.cb_histeq_gray.configure(
            cursor="hand2", font="{verdana} 10 {}", text="Gray"
        )
        self.cb_histeq_gray.pack(padx="2", pady="2", side="left")
        self.cb_histeq_bgr = tk.Checkbutton(self.frame_equalizationhist)
        self.cb_histeq_bgr.configure(cursor="hand2", text="BGR")
        self.cb_histeq_bgr.pack(padx="2", pady="2", side="left")
        self.frame_equalizationhist.configure(
            height="200", relief="groove", width="200"
        )
        self.frame_equalizationhist.pack(
            expand="false", fill="x", padx="5", pady="2", side="top"
        )
        self.frame_gamma_correction = ttk.Frame(
            self.scrolledframe_nb_imgprocessing.innerframe
        )
        self.frame_gamma_sub = ttk.Frame(self.frame_gamma_correction)
        self.lb_gc_gamma = ttk.Label(self.frame_gamma_sub)
        self.lb_gc_gamma.configure(text="Gamma")
        self.lb_gc_gamma.pack(padx="5", side="left")
        self.spinbox_gamma = ttk.Spinbox(self.frame_gamma_sub)
        self.spinbox_gamma.configure(
            cursor="hand2", from_="0", increment="0.1", to="10"
        )
        self.spinbox_gamma.configure(width="6")
        _text_ = """1"""
        self.spinbox_gamma.delete("0", "end")
        self.spinbox_gamma.insert("0", _text_)
        self.spinbox_gamma.pack(side="left")
        self.lb_gc_min = ttk.Label(self.frame_gamma_sub)
        self.lb_gc_min.configure(text="Min")
        self.lb_gc_min.pack(padx="5", side="left")
        self.spinbox_gc_min = ttk.Spinbox(self.frame_gamma_sub)
        self.spinbox_gc_min.configure(cursor="hand2", from_="0", to="127", width="6")
        _text_ = """0"""
        self.spinbox_gc_min.delete("0", "end")
        self.spinbox_gc_min.insert("0", _text_)
        self.spinbox_gc_min.pack(side="left")
        self.lb_gc_max = ttk.Label(self.frame_gamma_sub)
        self.lb_gc_max.configure(text="Max")
        self.lb_gc_max.pack(padx="5", side="left")
        self.spinbox_gc_max = ttk.Spinbox(self.frame_gamma_sub)
        self.spinbox_gc_max.configure(cursor="hand2", from_="127", to="255", width="6")
        _text_ = """255"""
        self.spinbox_gc_max.delete("0", "end")
        self.spinbox_gc_max.insert("0", _text_)
        self.spinbox_gc_max.pack(side="left")
        self.frame_gamma_sub.configure(height="200", width="200")
        self.frame_gamma_sub.pack(fill="x", padx="5", pady="5", side="top")
        self.cb_adjust_gamma = tk.Checkbutton(self.frame_gamma_correction)
        self.cb_adjust_gamma.configure(cursor="hand2", text="Adjust Gamma")
        self.cb_adjust_gamma.pack(anchor="sw", padx="2", pady="2", side="bottom")
        self.frame_gamma_correction.configure(height="200", width="200")
        self.frame_gamma_correction.pack(fill="x", padx="5", pady="5", side="top")
        self.frame_canny = ttk.Frame(self.scrolledframe_nb_imgprocessing.innerframe)
        self.cb_canny = tk.Checkbutton(self.frame_canny)
        self.cb_canny.configure(
            cursor="hand2", font="{verdana} 10 {}", text="Canny Edge"
        )
        self.cb_canny.pack(anchor="nw", padx="5", pady="5", side="top")
        self.lb_canny_min = ttk.Label(self.frame_canny)
        self.lb_canny_min.configure(text="Min")
        self.lb_canny_min.pack(anchor="w", padx="5", pady="5", side="left")
        self.sb_canny_min = ttk.Spinbox(self.frame_canny)
        self.sb_canny_min.configure(from_="0", to="126", width="10")
        self.sb_canny_min.pack(anchor="w", pady="5", side="left")
        self.lb_canny_max = ttk.Label(self.frame_canny)
        self.lb_canny_max.configure(text="Max")
        self.lb_canny_max.pack(padx="5", pady="5", side="left")
        self.sb_canny_max = ttk.Spinbox(self.frame_canny)
        self.sb_canny_max.configure(from_="127", to="255", width="10")
        self.sb_canny_max.pack(pady="5", side="left")
        self.frame_canny.configure(height="200", width="200")
        self.frame_canny.pack(fill="x", padx="5", pady="10", side="top")
        self.scrolledframe_nb_imgprocessing.innerframe.configure(relief="groove")
        self.scrolledframe_nb_imgprocessing.configure(usemousewheel=True)
        self.scrolledframe_nb_imgprocessing.pack(
            expand="true", fill="both", padx="2", pady="2", side="left"
        )
        self.notebook_frame_left.add(
            self.scrolledframe_nb_imgprocessing, text="Image Processing"
        )
        self.frame_nb_shot = ttk.Frame(self.notebook_frame_left)
        self.frame_materialname = ttk.Frame(self.frame_nb_shot)
        self.lb_materialname = ttk.Label(self.frame_materialname)
        self.lb_materialname.configure(font="{Arial} 10 {}", text="Material Name")
        self.lb_materialname.pack(anchor="nw", padx="5", pady="2", side="top")
        self.tb_materialname = ttk.Entry(self.frame_materialname)
        self.tb_materialname.configure(cursor="xterm")
        self.tb_materialname.pack(
            anchor="nw", expand="false", fill="x", padx="5", side="top"
        )
        self.tb_materialname.bind("<Return>", self.get_materialname, add="")
        self.frame_materialname.configure(borderwidth="2", height="200", width="200")
        self.frame_materialname.pack(
            anchor="nw", expand="false", fill="x", padx="5", pady="2", side="top"
        )
        self.frame_framenumber = ttk.Frame(self.frame_nb_shot)
        self.lb_framenumber = ttk.Label(self.frame_framenumber)
        self.lb_framenumber.configure(font="{Arial} 10 {}", text="Frame Number")
        self.lb_framenumber.pack(anchor="w", padx="5", pady="2", side="top")
        self.tb_framenumber = ttk.Entry(self.frame_framenumber)
        self.tb_framenumber.configure(cursor="xterm")
        self.tb_framenumber.pack(anchor="w", padx="5", side="left")
        self.tb_framenumber.bind("<Return>", self.get_framenumber, add="")
        self.btn_shot = tk.Button(self.frame_framenumber)
        self.btn_shot.configure(
            activebackground="#2c2c2c",
            activeforeground="#dedede",
            background="#2c2c2c",
            borderwidth="0",
        )
        self.btn_shot.configure(
            cursor="hand2",
            font="{Verdana} 12 {bold}",
            foreground="#dedede",
            text="Shot",
        )
        self.btn_shot.pack(anchor="center", padx="5", pady="5", side="right")
        self.btn_shot.configure(command=self.shot)
        self.frame_framenumber.configure(borderwidth="2", height="100", width="200")
        self.frame_framenumber.pack(
            anchor="nw", expand="false", fill="x", padx="5", side="top"
        )
        self.labelframe_outdata = ttk.Labelframe(self.frame_nb_shot)
        self.text_outdata = tk.Text(self.labelframe_outdata)
        self.text_outdata.configure(
            background="#000000",
            font="{Verdana} 10 {}",
            foreground="#cccccc",
            height="10",
        )
        self.text_outdata.configure(width="50")
        self.text_outdata.pack(expand="true", fill="both", side="top")
        self.labelframe_outdata.configure(height="200", text="Outdata", width="200")
        self.labelframe_outdata.pack(expand="true", fill="both", side="top")
        self.frame_nb_shot.configure(height="200", width="200")
        self.frame_nb_shot.pack(fill="y", side="top")
        self.notebook_frame_left.add(self.frame_nb_shot, text="Shot")
        self.notebook_frame_left.configure(height="200", width="200")
        self.notebook_frame_left.pack(expand="true", fill="both", side="top")
        self.panedwindow_body.add(self.notebook_frame_left, weight="1")
        self.scrolledframe_right = ScrolledFrame(
            self.panedwindow_body, scrolltype="both"
        )
        self.canvas_image = tk.Canvas(self.scrolledframe_right.innerframe)
        self.canvas_image.configure(
            background="#ffffff",
            confine="false",
            height="1200",
            highlightbackground="#ffffff",
        )
        self.canvas_image.configure(width="1920")
        self.canvas_image.pack(anchor="center", expand="true", fill="both", side="top")
        self.scrolledframe_right.configure(usemousewheel=True)
        self.scrolledframe_right.pack(
            expand="true", fill="both", padx="20", pady="10", side="left"
        )
        self.panedwindow_body.add(self.scrolledframe_right, weight="3")
        self.panedwindow_body.configure(width="200")
        self.panedwindow_body.pack(expand="true", fill="both", side="top")
        self.frame_body.configure(
            borderwidth="3", height="200", relief="flat", width="200"
        )
        self.frame_body.pack(expand="true", fill="both", side="top")
        self.add(self.frame_body, weight="24")
        self.frame_bottom = ttk.Frame(self)
        self.frame_infopanel = ttk.Frame(self.frame_bottom)
        self.panedwindow_infopanel = ttk.Panedwindow(
            self.frame_infopanel, orient="horizontal"
        )
        self.frame_shapei = ttk.Frame(self.panedwindow_infopanel)
        self.lb_shape = ttk.Label(self.frame_shapei)
        self.lb_shape.configure(font="{Arial} 10 {bold}", text="Shape:")
        self.lb_shape.pack(expand="false", side="left")
        self.lb_shapeval = ttk.Label(self.frame_shapei)
        self.lb_shapeval.configure(
            background="#ffffff", font="{Arial} 10 {}", text="0x0"
        )
        self.lb_shapeval.pack(expand="false", padx="5", side="left")
        self.frame_shapei.configure(height="200", relief="flat", width="200")
        self.frame_shapei.pack(side="top")
        self.panedwindow_infopanel.add(self.frame_shapei, weight="1")
        self.frame_minmax = ttk.Frame(self.panedwindow_infopanel)
        self.lb_min = ttk.Label(self.frame_minmax)
        self.lb_min.configure(font="{Arial} 10 {bold}", text="Min:")
        self.lb_min.pack(side="left")
        self.lb_minval = ttk.Label(self.frame_minmax)
        self.lb_minval.configure(background="#ffffff", font="{Arial} 10 {}", text="0")
        self.lb_minval.pack(padx="5", side="left")
        self.lb_max = ttk.Label(self.frame_minmax)
        self.lb_max.configure(font="{Arial} 10 {bold}", text="Max:")
        self.lb_max.pack(side="left")
        self.lb_maxval = ttk.Label(self.frame_minmax)
        self.lb_maxval.configure(background="#ffffff", font="{Arial} 10 {}", text="0")
        self.lb_maxval.pack(side="left")
        self.frame_minmax.configure(height="200", relief="flat", width="200")
        self.frame_minmax.pack(side="top")
        self.panedwindow_infopanel.add(self.frame_minmax, weight="1")
        self.frame_meani = ttk.Frame(self.panedwindow_infopanel)
        self.lb_mean = ttk.Label(self.frame_meani)
        self.lb_mean.configure(font="{Arial} 10 {bold}", text="Mean:")
        self.lb_mean.pack(side="left")
        self.lb_meanval = ttk.Label(self.frame_meani)
        self.lb_meanval.configure(background="#ffffff", font="{Arial} 10 {}", text="0")
        self.lb_meanval.pack(padx="5", side="left")
        self.frame_meani.configure(height="200", width="200")
        self.frame_meani.pack(side="top")
        self.panedwindow_infopanel.add(self.frame_meani, weight="1")
        self.frame_framenumberi = ttk.Frame(self.panedwindow_infopanel)
        self.lb_framenumberi = ttk.Label(self.frame_framenumberi)
        self.lb_framenumberi.configure(font="{Arial} 10 {bold}", text="FrameNumber:")
        self.lb_framenumberi.pack(side="left")
        self.lb_framenumberval = ttk.Label(self.frame_framenumberi)
        self.lb_framenumberval.configure(
            background="#ffffff", font="{Arial} 10 {}", text="0"
        )
        self.lb_framenumberval.pack(padx="5", side="left")
        self.frame_framenumberi.configure(height="200", width="200")
        self.frame_framenumberi.pack(side="top")
        self.panedwindow_infopanel.add(self.frame_framenumberi, weight="1")
        self.frame_ffgzi = ttk.Frame(self.panedwindow_infopanel)
        self.lb_ffgz = ttk.Label(self.frame_ffgzi)
        self.lb_ffgz.configure(font="{Arial} 10 {bold}", text="FF_GZ:")
        self.lb_ffgz.pack(side="left")
        self.lb_ffgzval = ttk.Label(self.frame_ffgzi)
        self.lb_ffgzval.configure(background="#ffffff", font="{Arial} 10 {}", text="0")
        self.lb_ffgzval.pack(padx="5", side="left")
        self.frame_ffgzi.configure(height="200", width="200")
        self.frame_ffgzi.pack(side="top")
        self.panedwindow_infopanel.add(self.frame_ffgzi, weight="1")
        self.panedwindow_infopanel.configure(height="20", width="200")
        self.panedwindow_infopanel.pack(fill="both", side="top")
        self.frame_infopanel.configure(height="200", width="200")
        self.frame_infopanel.pack(
            expand="false", fill="x", padx="10", pady="6", side="top"
        )
        self.frame_footer = ttk.Frame(self.frame_bottom)
        self.notebook_footer = ttk.Notebook(self.frame_footer)
        self.txt_log = tk.Text(self.notebook_footer)
        self.txt_log.configure(background="#000000", foreground="#00ff00")
        self.txt_log.pack(side="top")
        self.notebook_footer.add(self.txt_log, text="Message Log")
        self.frame_nbcompare = ttk.Frame(self.notebook_footer)
        self.frame_path_chooser = ttk.Frame(self.frame_nbcompare)
        self.tb_orig_data_path = ttk.Entry(self.frame_path_chooser)
        self.tb_orig_data_path.configure(state="disabled")
        self.tb_orig_data_path.pack(
            expand="true", fill="x", padx="5", pady="5", side="left"
        )
        self.btn_choose_orig_data = tk.Button(self.frame_path_chooser)
        self.btn_choose_orig_data.configure(
            activebackground="#a3d3f8",
            background="#a3d3f8",
            borderwidth="0",
            cursor="hand2",
        )
        self.btn_choose_orig_data.configure(font="{Verdana} 10 {}", text=".....")
        self.btn_choose_orig_data.pack(padx="5", pady="5", side="left")
        self.btn_choose_orig_data.configure(command=self.choose_original_data)
        self.frame_path_chooser.configure(height="200", width="200")
        self.frame_path_chooser.pack(fill="x", padx="5", pady="5", side="top")
        self.frame_plotcompare = ttk.Frame(self.frame_nbcompare)
        self.frame_plotcompare.configure(height="200", width="200")
        self.frame_plotcompare.pack(
            expand="true", fill="both", padx="5", pady="10", side="left"
        )
        self.frame_compare_buttons = ttk.Frame(self.frame_nbcompare)
        self.frame_btncompare = ttk.Frame(self.frame_compare_buttons)
        self.btn_compare = tk.Button(self.frame_btncompare)
        self.btn_compare.configure(
            activebackground="#232323",
            activeforeground="#ffffff",
            background="#232323",
            borderwidth="0",
        )
        self.btn_compare.configure(
            cursor="hand2",
            font="{Verdana} 10 {}",
            foreground="#ffffff",
            state="disabled",
        )
        self.btn_compare.configure(text="Compare")
        self.btn_compare.pack(side="top")
        self.btn_compare.configure(command=self.compare)
        self.frame_btncompare.configure(height="200", width="200")
        self.frame_btncompare.pack(padx="10", pady="10", side="top")
        self.frame_compare_buttons.configure(height="200", width="200")
        self.frame_compare_buttons.pack(
            expand="false", fill="both", padx="5", pady="5", side="right"
        )
        self.frame_nbcompare.configure(height="200", width="200")
        self.frame_nbcompare.pack(expand="true", fill="x", side="top")
        self.notebook_footer.add(self.frame_nbcompare, text="Compare")
        self.frame_livehistogram = ttk.Frame(self.notebook_footer)
        self.frame_livehistogram.configure(height="200", width="200")
        self.frame_livehistogram.pack(side="top")
        self.notebook_footer.add(self.frame_livehistogram, text="Live Histogram")
        self.notebook_footer.configure(height="200", width="200")
        self.notebook_footer.pack(expand="true", fill="both", side="bottom")
        self.frame_footer.configure(relief="groove")
        self.frame_footer.pack(expand="true", fill="both", side="top")
        self.frame_bottom.configure(relief="groove")
        self.frame_bottom.pack(side="top")
        self.add(self.frame_bottom, weight="4")
        self.configure(height="800", width="1000")
        self.pack(expand="true", fill="both", padx="5", pady="5", side="top")

    def save(self):
        pass

    def browse(self):
        pass

    def get_scalevar(self, event=None):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def show_current_img_histogram(self):
        pass

    def get_threshval(self, event=None):
        pass

    def get_kernel(self, event=None):
        pass

    def get_contrastval(self, event=None):
        pass

    def get_brightval(self, event=None):
        pass

    def get_colorspace(self, event=None):
        pass

    def select_morph_opr(self, event=None):
        pass

    def select_blur_type(self, event=None):
        pass

    def select_sharping(self, event=None):
        pass

    def get_threshtype(self, event=None):
        pass

    def get_materialname(self, event=None):
        pass

    def get_framenumber(self, event=None):
        pass

    def shot(self):
        pass

    def choose_original_data(self):
        pass

    def compare(self):
        pass

