'''
Base camera class module
'''
import cv2 as cv
import numpy as np


class Camera:
    def __init__(self, *args, **kwargs):
        pass

    def get_origin_frames(self):
        pass

    def __del__(self):
        pass

    def resize_frame(self, img, scale_percent=30):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        # resize image
        resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
        return resized

    def get_frame_foreground(self, frame, *args, **kwargs):
        '''Extract object from original frame '''
        try:
            THRESHVAL = 10
            kernel = (7, 7)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            if 'kernel' in kwargs:
                kernel = kwargs['kernel']
            if 'threshval' in kwargs:
                THRESHVAL = kwargs['threshval']
            blur = cv.GaussianBlur(gray, kernel, sigmaX=0, sigmaY=0)
            threshold_type = cv.THRESH_BINARY+cv.THRESH_OTSU
            th_val, thresh = cv.threshold(blur,
                                          0, 255,
                                          threshold_type)
            ret, mask = cv.threshold(gray,
                                     thresh=th_val+THRESHVAL,
                                     maxval=255,
                                     type=cv.THRESH_BINARY)
            frame_foreground = cv.bitwise_and(frame, frame, mask=mask)
            return frame_foreground
        except Exception as exc:
            raise exc

    def remove_noises(self, frame, *args, **kwargs):
        try:
            '''remove noises from original frame '''
            kernel = 7
            medianblurred = cv.medianBlur(frame, kernel)
            gray = cv.cvtColor(medianblurred, cv.COLOR_BGR2GRAY)
            minval = (gray[gray > 0]).min()
            ret, mask = cv.threshold(gray, thresh=minval, maxval=255,
                                        type=cv.THRESH_BINARY)

            resultframe = cv.bitwise_and(frame, frame, mask=mask)
            return resultframe
        except Exception as exc:
            raise exc

    def get_frame_foreground_mean(self, frame_foreground):
        '''return mean of extracted frame foreground '''
        # get non zero pixels
        ff_gz = frame_foreground[frame_foreground > 0]
        if ff_gz.size != 0:
            ffg_mean = ff_gz.sum() / ff_gz.size
            ffg_mean = round(ffg_mean, 3)
        else:
            ffg_mean = 0

        return ffg_mean

    def get_ffgz_size_min_max(self, frame_foreground):
        ff_gz = frame_foreground[frame_foreground > 0]
        if ff_gz.size != 0:
            return (ff_gz.size, ff_gz.min(), ff_gz.max())
        return (0, 0, 0)

    def get_orig_mean(self, orig):
        pass

    def get_contrasted_frame(self, frame, *args, **kwargs):
        if 'alpha' in kwargs:
            alpha = float(kwargs['alpha'])
        if 'beta' in kwargs:
            beta = float(kwargs['beta'])
        # contrasted = cv.addWeighted(
        #     src1=frame,
        #     alpha=alpha,
        #     src2=np.zeros(frame.shape, frame.dtype),
        #     beta=beta,
        #     gamma=0)
        contrasted = cv.convertScaleAbs(frame, alpha=alpha, beta=beta)
        return contrasted

    def clahe_gray_frame(self, frame, clipLimit=2.0, tileGridSize=(8, 8)):
        clahe = cv.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        # create a CLAHE object (Arguments are optional).
        frame = clahe.apply(frame)
        return frame

    def clahe_frame(self, frame, channels, clipLimit=2.0, tileGridSize=(8, 8)):
        clahe = cv.createCLAHE(clipLimit=clipLimit, tileGridSize=tileGridSize)
        ch1, ch2, ch3 = cv.split(frame)
        if channels[0]:
            ch1 = clahe.apply(ch1)
        if channels[1]:
            ch2 = clahe.apply(ch2)
        if channels[2]:
            ch3 = clahe.apply(ch3)
        frame = cv.merge((ch1, ch2, ch3))
        return frame

    def apply_image_canny_edge(self, frame, min, max):
        frame = cv.Canny(frame, min, max)
        return frame

    def get_frame_as_rgb(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        return frame
    def get_frame_as_gray(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        return frame

    def get_frame_as_lab(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2LAB)
        return frame

    def get_frame_as_hsv(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        return frame

    def get_frame_as_yuv(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2YUV)
        return frame

    def get_frame_as_ycrcb(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)
        return frame

    def get_frame_as_luv(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2Luv)
        return frame

    def get_frame_as_hls(self, frame):
        frame = cv.cvtColor(frame, cv.COLOR_BGR2HLS)
        return frame

    def equalize_gray_frame(self, grayframe):
        frame = cv.equalizeHist(grayframe)
        return frame

    def equalize_frame(self, frame, channels):
        ch1, ch2, ch3 = cv.split(frame)
        if channels[0]:
            ch1 = cv.equalizeHist(ch1)
        if channels[1]:
            ch2 = cv.equalizeHist(ch2)
        if channels[2]:
            ch3 = cv.equalizeHist(ch3)
        frame = cv.merge((ch1, ch2, ch3))
        return frame

    def equalize_hsv_frame(self, hsv_frame):
        # Histogram equalisation on the V-channel
        hsv_frame[:, :, 2] = cv.equalizeHist(hsv_frame[:, :, 2])
        frame = cv.cvtColor(hsv_frame, cv.COLOR_HSV2BGR)
        return frame

    def equalize_hls_frame(self, hls_frame):
        # Histogram equalisation on the S-channel
        hls_frame[:, :, 2] = cv.equalizeHist(hls_frame[:, :, 2])
        frame = cv.cvtColor(hls_frame, cv.COLOR_HLS2BGR)
        return frame

    def equalize_yuv_frame(self, yuv_frame):
        # equalize the histogram of the Y channel
        yuv_frame[:, :, 0] = cv.equalizeHist(yuv_frame[:, :, 0])
        frame = cv.cvtColor(yuv_frame, cv.COLOR_YUV2BGR)
        return frame

    def equalize_lab_frame(self, lab_frame):
        # equalize the histogram of the L channel
        L, a, b = cv.split(lab_frame)
        L = cv.equalizeHist(L)
        lab_frame = cv.merge((L, a, b))
        frame = cv.cvtColor(lab_frame, cv.COLOR_LAB2BGR)
        return frame

    def equalize_luv_frame(self, luv_frame):
        # equalize the histogram of the Y channel
        luv_frame[:, :, 0] = cv.equalizeHist(luv_frame[:, :, 0])
        frame = cv.cvtColor(luv_frame, cv.COLOR_Luv2BGR)
        return frame

    def equalize_ycrcb_frame(self, ycrcb_frame):
        y, cr, cb = cv.split(ycrcb_frame)
        # Applying equalize Hist operation on Y channel.
        y_eq = cv.equalizeHist(y)
        frame = cv.merge((y_eq, cr, cb))
        frame = cv.cvtColor(frame, cv.COLOR_YCR_CB2BGR)
        return frame

    def equalize_BGR_frame(self, frame):
        b, g, r = cv.split(frame)
        b = cv.equalizeHist(b)
        g = cv.equalizeHist(g)
        r = cv.equalizeHist(r)
        frame = cv.merge((b, g, r))
        return frame

    def split_frame_as_bgr(self, frame):
        b, g, r = cv.split(frame)
        return (b, g, r)

    def get_image_erosion(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        erosion = cv.erode(frame, kernel, iterations=1)
        return erosion

    def get_image_dilation(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        dilation = cv.dilate(frame, kernel, iterations=1)
        return dilation

    def get_image_opening(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        opening = cv.morphologyEx(frame, cv.MORPH_OPEN, kernel)
        return opening

    def get_image_closing(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        closing = cv.morphologyEx(frame, cv.MORPH_CLOSE, kernel)
        return closing

    def get_image_morph_gradient(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        gradient = cv.morphologyEx(frame, cv.MORPH_GRADIENT, kernel)
        return gradient

    def get_image_tophat(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        tophat = cv.morphologyEx(frame, cv.MORPH_TOPHAT, kernel)
        return tophat

    def get_image_blackhat(self, frame, kernelsize=(5, 5)):
        kernel = np.ones(kernelsize, np.uint8)
        blackhat = cv.morphologyEx(frame, cv.MORPH_BLACKHAT, kernel)
        return blackhat

    def get_image_gradient_laplacian(self, frame):
        laplacian = cv.Laplacian(frame, cv.CV_64F)
        return laplacian

    def get_image_gradient_sobelx(self, frame):
        sobelx = cv.Sobel(frame, cv.CV_64F, 1, 0, ksize=5)
        return sobelx

    def get_image_gradient_sobely(self, frame):
        sobely = cv.Sobel(frame, cv.CV_64F, 0, 1, ksize=5)
        return sobely

    def sharpen_frame_1(self, frame):
        kernel_sharpen_1 = np.array(
            [[0, -1, 0],
             [-1, 5, -1],
             [0, -1, 0]])
        sharpened = cv.filter2D(frame, -1, kernel_sharpen_1)
        return sharpened

    def sharpen_frame_2(self, frame):
        kernel_sharpen_2 = np.array(
            [[-1, -1, -1],
             [-1, 9, -1],
             [-1, -1, -1]])
        sharpened = cv.filter2D(frame, -1, kernel_sharpen_2)
        return sharpened

    def sharpen_frame_3(self, frame):
        kernel_sharpen_3 = np.array(
            [[1, 1, 1],
             [1, -7, 1],
             [1, 1, 1]])
        sharpened = cv.filter2D(frame, -1, kernel_sharpen_3)
        return sharpened

    def sharpen_frame_4(self, frame):
        kernel_sharpen_4 = np.array(
            [[-1, -1, -1, -1, -1],
             [-1, 2, 2, 2, -1],
             [-1, 2, 8, 2, -1],
             [-1, 2, 2, 2, -1],
             [-1, -1, -1, -1, -1]]) / 8.0
        sharpened = cv.filter2D(frame, -1, kernel_sharpen_4)
        return sharpened

    def adjust_gamma_grayframe(self, image, gamma=1.5, minval=0, maxval=255):
        invGamma = 1.0 / gamma
        table = np.array([((i / float(maxval)) ** invGamma) * maxval
                          for i in np.arange(minval, maxval+1)]).astype("uint8")
        adjusted = cv.LUT(image, table)
        return adjusted

    def adjust_gamma(self, image, gamma=1.5, minval=0, maxval=255):
        try:
            # build a lookup table mapping the pixel values [0, 255] to
            # their adjusted gamma values
            invGamma = 1.0 / gamma
            table = np.array([((i / float(maxval)) ** invGamma) * maxval
                              for i in np.arange(minval, maxval+1)]).astype("uint8")

            adjusted = cv.LUT(image, table)
            return adjusted
        except Exception as exc:
            print(f"adjust_gamma: {exc}")

    def apply_auto_contrast_bright(self, frame):
        '''auto contrast brightness '''
        alow = frame.min()
        ahigh = frame.max()
        amax = 255
        amin = 0
        # calculate alpha, beta
        alpha = ((amax - amin) / (ahigh - alow))
        beta = amin - alow * alpha
        # perform the operation g(x,y)= α * f(x,y)+ β
        new_img = cv.convertScaleAbs(frame, alpha=alpha, beta=beta)
        # return (new_img, alpha, beta)
        return new_img
