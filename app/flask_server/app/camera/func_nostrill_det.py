import cv2

import numpy as np

import pyrealsense2 as rs

from app.camera.cam import Camera

from keras.models import load_model

from keras.preprocessing.image import load_img, img_to_array, array_to_img

import matplotlib.pyplot as plt


class NostrillDet(Camera):
    @classmethod
    def init(cls):
        cls.net = load_model('app/camera/settings/net_model3')
    
    @classmethod
    def stop(cls):
        cls.pipeline.stop()
    
    @classmethod
    def start(cls):
        # allows us to access methods of the base class -> "Camera"
        super(NostrillDet, cls).start()
        cls.init()

    @staticmethod
    def __mask_input(input_image, mask):
        mask = np.dstack([mask] * 3)
        mask = (mask == 1)
        return np.where(mask, input_image, (255,0,0))

    @classmethod
    def scan_nostrill(cls):
        frames = cls.pipeline.wait_for_frames()
        
        aligned_frames = cls.align.process(frames)

        color_frame = aligned_frames.get_color_frame()                
        color_image = np.asanyarray(color_frame.get_data())

        depth_frame = aligned_frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())

        img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        img_in = img

        img = img_to_array(img)
        img = np.expand_dims(img, axis = 0)

        t = cls.net.predict(img)

        mask = np.argmax(t[0], axis = -1)
        mask = np.expand_dims(mask, axis = -1)

        n_1 = np.where(mask == 0)

        n_2 = np.where(mask == 2)
        

        try:
            centroide1 = (sum(n_1[0]) / len(n_1[0]), sum(n_1[1]) / len(n_1[1]))
            print("Center of right nostril: " + str(centroide1))

            centroide2 = (sum(n_2[0]) / len(n_2[0]), sum(n_2[1]) / len(n_2[1]))
            print("Center of left nostril: " + str(centroide2))
        
            x = int(centroide1[1])
            y = int(centroide1[0])

            color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
            
            depth = depth_frame.get_distance(x, y)

            dx ,dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x,y], depth)

            return [dx, dy, dz]

        except ZeroDivisionError:
            print("Nelze urcit!")
    

        # masked_img = cls.__mask_input(img_in, mask)
        
        
        # plt.imshow(masked_img)
        # plt.scatter([centroide1[1], centroide2[1]], [centroide1[0], centroide2[0]], color = 'b')
        # plt.show()
        
        # cls.stop()
