# library -> python wrapper for intel realsense camera
import pyrealsense2 as rs

# library -> numpy data manage
import numpy as np

# script -> inicialized camera setting
from app.camera.cam import Camera

class TakePC(Camera):
    # private classmethod:
    #   input: none
    #   return none
    # Note: Set up path for saving pointclouds
    @classmethod
    def __path(self):
        return "camera/pointclouds"

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
        super(TakePC, self).start_pc()
    
    # !!public classmethod:
    #   input: none
    #   return none
    # Note: in progress!!
    @classmethod
    def take_pointcloud(self):
        path = "app/camera/pointclouds"

        # for i in range ... 
        # there could be communication with robot 
        for x in range(2):

            c = 0
            while 1:
                frames = self.pipeline.wait_for_frames()
                frames.first(self.other_stream).as_video_frame()
                
                c+=1

                if c == 20:
                    ply = rs.save_to_ply(path + '/point_cloud_%d.ply' % x)
                    
                    ply.set_option(rs.save_to_ply.option_ply_binary, False)
                    ply.set_option(rs.save_to_ply.option_ply_normals, True)

                    print("Saving...")

                    # Apply the processing block to the frameset which contains the depth frame and the texture
                    ply.process(frames)

                    break