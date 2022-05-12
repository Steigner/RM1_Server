# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# script -> inicialized camera setting
from app.camera.cam import Camera


class NostrillDet(Camera):
    # public classmethod:
    #   input: none
    #   return none
    # Note: Load pre-trained CNN model for detection of nostril
    @classmethod
    def __init_detection_model(cls):
        cls.net = cv2.dnn.readNetFromONNX("app/camera/settings/Unet.onnx")

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
        # allows us to access methods of the base class -> "Camera"
        super(NostrillDet, cls).start(align_to_dept=True)
        cls.__init_detection_model()

    # private classmethod:
    #   input: input image, mask image
    #   return segmented nostrils
    # Note: Parse output from CNN.
    @staticmethod
    def __mask_input(input_image, mask):
        mask = np.dstack([mask] * 3)
        mask = mask == 1
        return np.where(mask, input_image, (255, 0, 0))

    # public classmethod:
    #   input: none
    #   return x,y of center of nostril
    # Note: Parse output from CNN.
    @classmethod
    def scan_nostrill(cls):
        frames = cls.pipeline.wait_for_frames()

        aligned_frames = cls.align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        depth_frame = aligned_frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())

        # convert color
        img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # write depth and color image to folder as .jpg and .png
        cv2.imwrite("app/graph/face.jpg", color_image)
        cv2.imwrite("app/graph/face.png", depth_image)

        img = np.array([img]).astype("float64")

        # use pre-trained model in OpenCV
        cls.net.setInput(img)
        t = cls.net.forward()

        mask = np.argmax(t[0], axis=-1)
        mask = np.expand_dims(mask, axis=-1)

        # search from segmented image, area of left and right nostril
        n_1 = np.where(mask == 0)
        n_2 = np.where(mask == 2)

        try:
            # calculate centroid of right nostril
            centroide1 = (sum(n_1[0]) / len(n_1[0]), sum(n_1[1]) / len(n_1[1]))
            print("Center of right nostril: " + str(centroide1))

            # calculate centroid of left nostril
            centroide2 = (sum(n_2[0]) / len(n_2[0]), sum(n_2[1]) / len(n_2[1]))
            print("Center of left nostril: " + str(centroide2))
            
            x = int(centroide1[1])
            y = int(centroide1[0])

            return [x, y]

        except ZeroDivisionError:
            print("Cannot be detected!")
