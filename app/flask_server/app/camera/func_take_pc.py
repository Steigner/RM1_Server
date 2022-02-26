# library -> python wrapper for intel realsense camera
import pyrealsense2 as rs

# script -> inicialized camera setting
from app.camera.cam import Camera


class TakePC(Camera):
    # public classmethod:
    #   input: none
    #   return none
    # Note: Stop streaming camera
    @classmethod
    def stop(cls):
        cls.pipeline.stop()

    # public classmethod:
    #   input: none
    #   return none
    # Note: Start streaming camera
    @classmethod
    def start(cls):
        super(TakePC, cls).start_pc()

    # !!public classmethod:
    #   input: none
    #   return none
    # Note: in progress!!
    @classmethod
    def take_pointcloud(cls):
        path = "app/graph"

        c = 0
        while 1:
            frames = cls.pipeline.wait_for_frames()
            frames.first(cls.other_stream).as_video_frame()

            c += 1

            if c == 20:
                ply = rs.save_to_ply(path + "/point_cloud.ply")

                ply.set_option(rs.save_to_ply.option_ply_binary, False)
                ply.set_option(rs.save_to_ply.option_ply_normals, True)

                print("Saving...")

                # Apply the processing block to the frameset which contains the depth frame and the texture
                ply.process(frames)

                break

        # cls.stop()
