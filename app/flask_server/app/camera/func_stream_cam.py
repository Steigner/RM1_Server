# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# script -> inicialized camera setting
from app.camera.cam import Camera

class StreamCam(Camera):
    # public classmethod:
    #   input: none
    #   return none
    # Note: Stop streaming camera
    @classmethod
    def stop(self):
        self.pipeline.stop()
    
    # public classmethod:
    #   input: none
    #   return none
    # Note: Start streaming camera
    @classmethod
    def start(self):
        super(StreamCam, self).start() 
    
    # public classmethod:
    #   input: switch -> which streaming user choose
    #   return jpeg image of camera [jpg - tobytes]
    # Note: In this method we set the camera streaming options.
    #   switch = 0 -> color image
    #   switch = 1 -> depth image
    #   switch = 2 -> infra image
    @classmethod
    def get_frame(self, switch):
        frames = self.pipeline.wait_for_frames()
        
        aligned_frames = self.align.process(frames)
        
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        infra_frame = frames.first(self.infared_stream)
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        infra_image = np.asanyarray(infra_frame.get_data())

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # color_frame
        if switch == 0:
            jpeg = cv2.imencode('.jpg', color_image)[1].tobytes()
            return jpeg
        
        # depth_frame
        if switch == 1:
            jpeg = cv2.imencode('.jpg', depth_colormap)[1].tobytes()
            return jpeg
        
        # infra_frame
        if switch == 2:
            jpeg = cv2.imencode('.jpg', infra_image)[1].tobytes()
            return jpeg