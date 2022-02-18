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
    def __init(cls):
        cls.data = None
        cls.pipeline = None
        cls.align = None
        cls.infared_stream = None
        cls.other_stream = None

    # private classmethod:
    #   input: none
    #   return none
    # Note: warm up camera
    @classmethod
    def __warm_up(cls):
        time.sleep(2)
        for i in range(20):
            cls.pipeline.wait_for_frames()

    # public classmethod:
    #   input: none
    #   return none
    # Note: init camera, enable streaming modes, by most optional resolution and 
    # hardware FPS parameters. Please be carefull with changing this parametres, becouse it will raise
    # error and camera may not work properly.
    @classmethod
    def start(cls, align_to_dept=False):
        cls.__init()

        cls.pipeline = rs.pipeline()
        cls.infared_stream = rs.stream.infrared 
        
        config = rs.config()
        config.enable_stream(cls.infared_stream, 640, 480, rs.format.y8, 60)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 640,480, rs.format.bgr8, 60)

        cls.pipeline.start(config)
        
        if align_to_dept:
            align_to = rs.stream.depth
        
        else:
            align_to = rs.stream.color

        cls.align = rs.align(align_to)

        cls.__warm_up()
    
    @classmethod
    def start_color(cls):
        cls.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 360, rs.format.bgr8, 60)
        cls.pipeline.start(config)

        cls.__warm_up()

    # public classmethod:
    #   input: none
    #   return none
    # Note: init camera for taking point clouds, enable streaming modes, by most optional resolution and 
    # hardware FPS parameters. Please be carefull with changing this parametres, becouse it will raise
    # error and camera may not work properly.
    @classmethod
    def start_pc(cls):
        cls.__init()
        cls.pipeline = rs.pipeline()

        cls.other_stream, other_format = rs.stream.color, rs.format.rgb8

        config = rs.config()
        config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
        config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        config.enable_stream(cls.other_stream, 848, 480, other_format, 60)

        cls.pipeline.start(config)
        cls.__warm_up()