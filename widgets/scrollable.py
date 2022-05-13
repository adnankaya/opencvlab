import tkinter as tk

# ************************
# Scrollable Frame Class
# ************************
DELAY = 100


class ScrollFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # place canvas on self
        self.canvas = tk.Canvas(self, borderwidth=0, background="#000000")
        # place a frame on the canvas, this frame will hold the child widgets
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        # place a scrollbar on self
        self.vsb = tk.Scrollbar(self, orient="vertical",
                                command=self.canvas.yview)
        # attach scrollbar action to scroll of canvas
        self.canvas.configure(yscrollcommand=self.vsb.set)

        # pack scrollbar to right of self
        self.vsb.pack(side="right", fill="y")
        # pack canvas to left of self and expand to fil
        self.canvas.pack(side="left", fill="both", expand=True)
        # add view port frame to canvas
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort,
                                                       anchor="nw",
                                                       tags="self.viewPort")

        # bind an event whenever the size of the viewPort frame changes.
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>", self.onCanvasConfigure)

        # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize
        self.onFrameConfigure(None)
        self.delay = DELAY

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        # whenever the size of the canvas changes alter the window region respectively.
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
