# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# script -> inicialized camera setting
from app.camera.cam import Camera


class FaceDet(Camera):
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
        super(FaceDet, cls).start()
        cls.__init_detection_model()

    # private classmethod:
    #   input: none
    #   return none
    # Note: inicialize opencv pretrained face detection models
    @classmethod
    def __init_detection_model(cls):
        LBFmodel = "app/camera/settings/lbfmodel.yaml"
        haarcascade_clf = "app/camera/settings/haarcascade_frontalface_alt2.xml"
        cls.detector = cv2.CascadeClassifier(haarcascade_clf)
        cls.landmark_detector = cv2.face.createFacemarkLBF()
        cls.landmark_detector.loadModel(LBFmodel)

    # private classmethod:
    #   input: color image [np.asarray]
    #   return position of landmarks [np.array], image with opencv changes [np.array]
    # Note: In this method is defined position of location for detection face.
    #   Main function is to handle if detected head landmarks is outside of inside defined zone.
    @classmethod
    def __show(cls, image):
        # defined zone
        x1 = 100
        y1 = 50
        x2 = 640 - 100
        y2 = 640 - 200

        # appned landmarks points
        # land = []

        # need to be color image converted to gray scale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect face
        faces = cls.detector.detectMultiScale(image_gray)

        # landmarks is not find
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # validation variable -> is use ass acces var
        cls.validation = False

        # get all landmark of array of finded face points
        for (x, y, w, d) in faces:
            _, landmarks = cls.landmark_detector.fit(image_gray, faces)

            # landmarks is in defined zone
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cls.validation = True

            # show all landrmarks points
            for landmark in landmarks:
                # land = landmark

                # land = [int(landmark[0][33][0]), int(landmark[0][33][1])]

                cv2.circle(
                    image,
                    (int(landmark[0][33][0]), int(landmark[0][33][1])),
                    4,
                    (255, 0, 0),
                    4,
                )

                for x, y in landmark[0]:
                    # (B-G-R)--thicknes
                    # due to compatibility to opencv version 5.2.1
                    cv2.circle(image, (int(x), int(y)), 1, (0, 0, 139), 2)

                    # if is face landmarks out of range
                    if x > x2 or y > y2 or x < x1 or y < y1:
                        # landmarks is out of defined zone
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

                        cls.validation = False

        return image

    # private classmethod:
    #   input: none
    #   return color image [np.asarray]
    # Note: inicialize camera and return color image from camera
    @classmethod
    def __image(cls):
        frames = cls.pipeline.wait_for_frames()

        aligned_frames = cls.align.process(frames)
        color_frame = aligned_frames.get_color_frame()
        image = np.asarray(color_frame.get_data())

        return image, aligned_frames

    # public classmethod:
    #   input: none
    #   return jpeg color modifed by __show() method [jpg - tobytes]
    # Note: get color image and put into __show() method, then return modified data.
    @classmethod
    def set_position(cls):
        image, aligned_frames = cls.__image()

        image_color = cls.__show(image)

        jpeg = cv2.imencode(".jpg", image_color)[1].tobytes()

        return jpeg

    # public classmethod:
    #   input: none
    #   return validation variable [bool]
    @classmethod
    def get_val(cls):
        return cls.validation
