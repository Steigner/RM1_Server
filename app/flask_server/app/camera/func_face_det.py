# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# script -> inicialized camera setting
from app.camera.cam import Camera

import pyrealsense2 as rs

class FaceDet(Camera):
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
        # allows us to access methods of the base class -> "Camera"
        super(FaceDet, self).start()
        self.__init_detection_model()
    
    # private classmethod:
    #   input: none
    #   return none
    # Note: inicialize opencv pretrained face detection models
    @classmethod
    def __init_detection_model(self):
        LBFmodel = "app/camera/settings/lbfmodel.yaml"
        haarcascade_clf = "app/camera/settings/haarcascade_frontalface_alt2.xml"
        self.detector = cv2.CascadeClassifier(haarcascade_clf)
        self.landmark_detector  = cv2.face.createFacemarkLBF()
        self.landmark_detector.loadModel(LBFmodel)

    # private classmethod:
    #   input: color image [np.asarray]
    #   return position of landmarks [np.array], image with opencv changes [np.array]
    # Note: In this method is defined position of location for detection face.
    #   Main function is to handle if detected head landmarks is outside of inside defined zone.
    @classmethod
    def __show(self, image):
        # defined zone
        x1 = 100
        y1 = 50
        x2 = 640 - 200
        y2 = 640 - 200

        # appned landmarks points 
        land = []
        
        # need to be color image converted to gray scale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect face 
        faces = self.detector.detectMultiScale(image_gray)
        
        # landmarks is not find
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        
        # validation variable -> is use ass acces var
        self.validation = False

        # get all landmark of array of finded face points 
        for (x, y, w, d) in faces:
            _, landmarks = self.landmark_detector.fit(image_gray, faces)
            
            # landmarks is in defined zone
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            self.validation = True
            
            # show all landrmarks points
            for landmark in landmarks:
                # land = landmark
                
                # land = [int(landmark[0][33][0]), int(landmark[0][33][1])]
                
                cv2.circle(image, (int(landmark[0][33][0]), int(landmark[0][33][1])), 4, (255, 0, 0), 4)

                for x,y in landmark[0]:
                    # (B-G-R)--thicknes 
                    # due to compatibility to opencv version 5.2.1
                    cv2.circle(image, (int(x), int(y)), 1, (0, 0, 139), 2)
                    
                    # if is face landmarks out of range    
                    if x > x2 or y > y2 or x < x1 or y <y1:
                        # landmarks is out of defined zone
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)       
                        
                        self.validation = False

        return image

    """
    # tohle nebude potreba jelikoz je to stare na porovnavani pozice xichtu !!!
    # 
    # !!private classmethod:
    #   input: color image [np.asarray], landmarks [np.array]
    #   return image with opencv changes [np.array]
    # Note: In this method we checking if user not move with his head.
    #   Basic approach of comparing saved array of landmarks to new detected landmarks. 
    #   In progress!!
    @classmethod
    def __validation_position(self, land, image):
        # opencv font
        font = cv2.FONT_HERSHEY_DUPLEX

        # need to be color image converted to gray scale        
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # detect face 
        faces = self.detector.detectMultiScale(image_gray)
        
        # show saved landmarks
        for x, y in land[0]:
            cv2.circle(image,(int(x), int(y)), 1, ((0, 255, 0)),5)
        
        tup, tup2 = [], []
        
        # show new detected landmarks
        for (x, y, w, d) in faces:
            _, landmarks = self.landmark_detector.fit(image_gray, faces)
            for landmark in landmarks:
                tup2 = np.array(landmark[0])
                for x,y in landmark[0]:
                    # due to compatibility to opencv version 5.2.1
                    cv2.circle(image, (int(x), int(y)), 1, (0, 0, 139), 2)     

        # compare landrmarks
        if np.size(tup2) > 0:
            tup = np.array(land[0]) 

            for i in range(len(land)):          
                dist = np.linalg.norm(tup[i]-tup2[i])            
                
                if dist > 5:
                    text = str("Wrong!")
                    
                else:
                    text = str("OK!")
        else:
            text = str("Dont find pattern")
        
        cv2.putText(image, text, (20,50), font, 0.75, (255, 255, 255), 1)
        return image
    """

    # private classmethod:
    #   input: none
    #   return color image [np.asarray]
    # Note: inicialize camera and return color image from camera
    @classmethod
    def __image(self):
        frames = self.pipeline.wait_for_frames()

        aligned_frames = self.align.process(frames) 
        color_frame = aligned_frames.get_color_frame()
        image = np.asarray(color_frame.get_data())
        
        return image, aligned_frames

    """
    should be deleted!!
    
    @classmethod
    def __computed_point(self, land, aligned_frames):
        depth_frame = aligned_frames.get_depth_frame()
        
        aligned_color_frame = aligned_frames.get_color_frame()
        
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics
        
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(aligned_color_frame.get_data())
        
        x, y = land[0], land[1] 

        depth = depth_frame.get_distance(x, y)
        
        dx ,dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x,y], depth)
        # print(dx,dy,dz)
        
        return [dx, dy, dz]
    """

    # public classmethod:
    #   input: none
    #   return jpeg color modifed by __show() method [jpg - tobytes]
    # Note: get color image and put into __show() method, then return modified data.
    @classmethod
    def set_position(self):            
        image, aligned_frames = self.__image()

        image_color = self.__show(image)
        
        jpeg = cv2.imencode('.jpg', image_color)[1].tobytes()

        return jpeg

    # public classmethod:
    #   input: none
    #   return validation variable [bool]
    @classmethod
    def get_val(self):
        return self.validation