import pyzed.sl as sl

class camara_zed():
    def __init__(self, res, fps):
        self.res = res
        self.fps = fps
        zed = sl.Camera()
        init_params = sl.InitParameters()
        self.zed = zed
        if res == 1080:
            init_params.camera_resolution = sl.RESOLUTION.HD1080
            init_params.camera_fps = self.fps
            self.zed.open()
        if res == 720:
            init_params.camera_resolution = sl.RESOLUTION.HD720
            init_params.camera_fps = self.fps
            self.zed.open()
    def close(self):
        self.zed.close()
    def grab(self):
        return self.zed.grab()
    def retrieve_image(self, a, b):
        return self.zed.retrieve_image(a, b)



