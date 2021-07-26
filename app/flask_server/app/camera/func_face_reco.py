# library -> The world's simplest facial recognition api
import face_recognition

# library -> opencv
import cv2

# library -> numpy data manage
import numpy as np

# library -> manage blob image from database
from io import BytesIO

# script -> inicialized camera setting
from app.camera.cam import Camera

class FaceReco(Camera):
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
        super(FaceReco,self).start()
        self.validation = False

    # public classmethod:
    #   input: color image [!!], name [string]
    #   return none
    # Note: inicialize photo and name for face recognition
    @classmethod
    def init_patient(self, image, name):
        patient_image = face_recognition.load_image_file(BytesIO(image))
        self.known_face_encodings = [face_recognition.face_encodings(patient_image)[0]]
        self.known_face_names = [name]

    # public classmethod:
    #   input: none
    #   return modifed color image [jpg - tobytes]
    # Note: 
    @classmethod    
    def recognize(self):
        frames = self.pipeline.wait_for_frames()
        
        # validation variable -> is use ass acces var
        self.validation = False

        #color_frame = frames.first(rs.stream.color)
        aligned_frames = self.align.process(frames) 
        color_frame = aligned_frames.get_color_frame()
        Color_image = np.asarray(color_frame.get_data())

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = Color_image[:, :, ::-1]
        
        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Loop through each face in this frame of video
        for (x, y, w, d), face_encoding in zip(face_locations, face_encodings):
            
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unautorized Person"

            # known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            # if match with photo with streaming image
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                self.validation = True

            # Draw a box around the face
            cv2.rectangle(Color_image, (d - 20 , x - 20), (y + 20, w + 20), (0, 0, 255), 2)

            # Draw Name
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(Color_image, name, (d - 20, w + 50), font, 0.75, (255, 255, 255), 1)
        
        jpeg = cv2.imencode('.jpg', Color_image)[1].tobytes()
        return jpeg

    # public classmethod:
    #   input: none
    #   return validation variable [bool]
    @classmethod
    def get_val(self):
        return self.validation