# library -> python wrapper for intel realsense camera
import pyrealsense2 as rs

# library -> time manage
import time

class Camera(object): 
    # private classmethod:
    #   input: none
    #   return none
    # Note: Init values
    @classmethod
    def __init(self):
        self.pipeline = None
        self.align = None
        self.infared_stream = None
        self.other_stream = None

    # private classmethod:
    #   input: none
    #   return none
    # Note: warm up camera
    @classmethod
    def __warm_up(self):
        time.sleep(2)
        for i in range(20):
            self.pipeline.wait_for_frames()

    # private classmethod:
    #   input: none
    #   return none
    # Note: init camera, enable streaming modes, by most optional resolution and 
    # hardware FPS parameters. Please be carefull with changing this parametres, becouse it will raise
    # error and camera may not work properly.
    @classmethod
    def start(self):
        self.__init()

        self.pipeline = rs.pipeline()
        self.infared_stream = rs.stream.infrared 
        
        config = rs.config()
        config.enable_stream(self.infared_stream, 640, 480, rs.format.y8, 60)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 60)

        self.pipeline.start(config)
        
        align_to = rs.stream.color
        self.align = rs.align(align_to)

        self.__warm_up()

    # private classmethod:
    #   input: none
    #   return none
    # Note: init camera for taking point clouds, enable streaming modes, by most optional resolution and 
    # hardware FPS parameters. Please be carefull with changing this parametres, becouse it will raise
    # error and camera may not work properly.
    @classmethod
    def start_pc(self):
        self.__init()
        self.pipeline = rs.pipeline()

        self.other_stream, other_format = rs.stream.color, rs.format.rgb8

        config = rs.config()
        config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        config.enable_stream(self.other_stream, 848, 480, other_format, 60)

        self.pipeline.start(config)
        self.__warm_up()
