# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# library -> QR code and AE 128 reader
from pyzbar import pyzbar

# script -> inicialized camera setting
from app.camera.cam import Camera


class ReadQR(Camera):
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
        super(ReadQR, cls).start()

    # public classmethod:
    #   input: none
    #   return decoded barcode data
    # Note: This method is used for get data and post to route
    @classmethod
    def output_data(cls):
        # !!!!!!!!!!!!!!!!!!!!!
        # exception for no data
        # data = cls.data
        data = cls.data
        return data

    # public classmethod:
    #   input: none
    #   return jpeg color image [jpg - tobytes]
    # Note: In this method we get color image, and on this image we decoded defined barcode,
    #   and store data to cls.data. Also we using opencv to draw frame for detected barcode.
    @classmethod
    def QR_code_reader(cls):
        frames = cls.pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        data = pyzbar.decode(color_image)

        if data:
            font = cv2.FONT_HERSHEY_DUPLEX

            # there is place for better visualitian etc ...
            for barcode in data:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(color_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            name = "QR-code loaded"
            cv2.putText(
                color_image,
                name,
                (354 - 20, 325 + 50),
                font,
                0.75,
                (255, 255, 255),
                1,
            )

            cls.data = data

        jpeg = cv2.imencode(".jpg", color_image)[1].tobytes()
        return jpeg
