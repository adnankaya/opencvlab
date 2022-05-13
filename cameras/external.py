
# internal
from .camera import Camera


class External(Camera):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __del__(self):
        pass

    
