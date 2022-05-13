import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def putText2Frame(frame, text, org):
    '''frame: object | image or captured frame
        text: string |
        org: tuple | coordiantes (x,y) '''
    cv.putText(frame,
               text,
               org=org,
               fontFace=cv.QT_FONT_NORMAL,
               fontScale=.6,
               color=(255, 255, 255),
               thickness=1,
               lineType=cv.LINE_AA)


def handleMouseEvent(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print(f"Left: x:{x}  y:{y}")
    if event == cv.EVENT_LBUTTONDBLCLK:
        pass


def annot_max(x, y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text = "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax = plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops = dict(
        arrowstyle="->", connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data', textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94, 0.96), **kw)
