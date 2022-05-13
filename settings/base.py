import os

THEMELIST = ['vista', 'clam', 'classic', 'default', 'alt']
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_FILE = 'settings.json'
BG_IMG = 'logo.png'
SETTINGS = {}

KERNELS = {
    '3': (3, 3),
    '5': (5, 5),
    '7': (7, 7),
    '9': (9, 9),
    '11': (11, 11),
    '13': (13, 13),
    '15': (15, 15),
    '17': (17, 17),
    '19': (19, 19),
    '21': (21, 21)
}

THRESH_TYPES = [
    'None',
    'binary',
    'binary_inv',
    'tozero',
    'tozero_inv',
    'trunc',
    'adaptive_thresh_mean_c',
    'adaptive_thresh_gaussian_c',
]

COLORSPACES = [
    'BGR',
    'RGB',
    'Gray',
    'HSV',
    'HLS',
    'CIELab',
    'YUV',
    'YCrCb',
    'Luv'
]

MORPHOLOGICAL_OPERATIONS = [
    'None', 'erosion', 'dilation',
    'opening', 'closing', 'gradient',
    'top hat', 'black hat'
]

SHARPENING_LIST = ["None", "sharpen1", "sharpen2", "sharpen3", "sharpen4"]

IMAGE_GRADIENTS = ['None', 'laplacian', 'sobelx', 'sobely']

BLUR_TYPES = ['None', 'blur',  'median', 'gaussian']
