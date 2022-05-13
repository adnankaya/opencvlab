'''
Default webcam
'''
import cv2 as cv
# internal
from .camera import Camera


class Webcam(Camera):
    def __init__(self, *args, **kwargs):
        Camera.__init__(self, *args, **kwargs)
        try:
            if not 'cam_source' in kwargs:
                self.camera = cv.VideoCapture(0)
            else:
                cam_source = kwargs['cam_source']
                self.camera = cv.VideoCapture(cam_source)
                if not self.camera.isOpened():
                    raise ValueError("Unable to open video source", cam_source)

            # Get video source width and height
            # self.camera.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
            # self.camera.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
            self.width = self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
            self.height = self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)

        except Exception as exc:
            raise exc

    def __del__(self):
        if self.camera.isOpened():
            self.camera.release()

    def get_origin_frames(self):
        '''returns received frame as BGR '''
        if self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
