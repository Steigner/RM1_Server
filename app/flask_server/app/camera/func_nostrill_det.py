import cv2

import numpy as np

from app.camera.cam import Camera

# import matplotlib.pyplot as plt


class NostrillDet(Camera):
    @classmethod
    def __init_detection_model(cls):
        cls.net = cv2.dnn.readNetFromONNX("app/camera/settings/nm_unet_1.onnx")

    @classmethod
    def stop(cls):
        cls.pipeline.stop()

    @classmethod
    def start(cls):
        # allows us to access methods of the base class -> "Camera"
        super(NostrillDet, cls).start(align_to_dept=True)
        cls.__init_detection_model()

    @staticmethod
    def __mask_input(input_image, mask):
        mask = np.dstack([mask] * 3)
        mask = mask == 1
        return np.where(mask, input_image, (255, 0, 0))

    @classmethod
    def scan_nostrill(cls):
        frames = cls.pipeline.wait_for_frames()

        aligned_frames = cls.align.process(frames)

        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        depth_frame = aligned_frames.get_depth_frame()
        depth_image = np.asanyarray(depth_frame.get_data())

        img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # plt.imshow(img)
        # plt.show()

        cv2.imwrite("app/graph/face.jpg", color_image)

        # plt.imshow(depth_image)
        # plt.show()

        cv2.imwrite("app/graph/face.png", depth_image)

        # img_in = img

        img = np.array([img]).astype("float64")

        # img = np.expand_dims(img, axis = 0)

        cls.net.setInput(img)
        t = cls.net.forward()

        mask = np.argmax(t[0], axis=-1)
        mask = np.expand_dims(mask, axis=-1)

        n_1 = np.where(mask == 0)

        n_2 = np.where(mask == 2)
        try:
            centroide1 = (sum(n_1[0]) / len(n_1[0]), sum(n_1[1]) / len(n_1[1]))
            print("Center of right nostril: " + str(centroide1))

            centroide2 = (sum(n_2[0]) / len(n_2[0]), sum(n_2[1]) / len(n_2[1]))
            print("Center of left nostril: " + str(centroide2))

            x = int(centroide1[1])
            y = int(centroide1[0])

            """
            masked_img = cls.__mask_input(img_in, mask)

            plt.imshow(masked_img)
            plt.scatter([centroide1[1], centroide2[1]], [centroide1[0], centroide2[0]], color = 'b')
            plt.show()

            plt.imshow(depth_image)
            plt.scatter([centroide1[1], centroide2[1]], [centroide1[0], centroide2[0]], color = 'b')
            plt.show()
            """

            return [x, y]

        except ZeroDivisionError:
            print("Cannot be detected!")
