# import cv2
# import itertools
# import numpy as np
# import mediapipe as mp

# class FaceMesh():
#     def __init__(self):
#         self.mpFaceDetection = mp.solutions.face_detection
#         self.face_detection = self.mpFaceDetection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
#         self.mpDraw = mp.solutions.drawing_utils
#         self.MpFaceMesh = mp.solutions.face_mesh
#         self.faceMeshImages = self.MpFaceMesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
#         self.faceMeshVideos = self.MpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.3)
#         self.mpDrawStyles = mp.solutions.drawing_styles

#     def detectFacialLandmarks(self, image, face_mesh):
#         results = face_mesh.process(image[:,:,::-1])  
#         output_image = image[:,:,::-1].copy()
#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 self.mpDraw.draw_landmarks(
#                     image=output_image,
#                     landmark_list=face_landmarks,
#                     connections=self.MpFaceMesh.FACEMESH_TESSELATION,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_tesselation_style()
#                 )
#                 self.mpDraw.draw_landmarks(
#                     image=output_image,
#                     landmark_list=face_landmarks,
#                     connections=self.MpFaceMesh.FACEMESH_CONTOURS,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_contours_style()
#                 )
#         return np.ascontiguousarray(output_image[:,:,::-1],dtype=np.uint8), results



# import cv2
# import numpy as np
# import itertools
# import mediapipe as mp

# class FaceMesh():
#     def __init__(self):
#         self.mpFaceDetection = mp.solutions.face_detection
#         self.face_detection = self.mpFaceDetection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
#         self.mpDraw = mp.solutions.drawing_utils
#         self.MpFaceMesh = mp.solutions.face_mesh
#         self.faceMeshImages = self.MpFaceMesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
#         self.faceMeshVideos = self.MpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.3)
#         self.mpDrawStyles = mp.solutions.drawing_styles

#     def detectFacialLandmarks(self, image, face_mesh):
#         # 1. Properly convert to RGB so MediaPipe gets the right dimensions
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = face_mesh.process(rgb_image)  
        
#         # 2. Work directly on a copy of the original BGR frame
#         output_image = image.copy()
        
#         if results.multi_face_landmarks:
#             for face_landmarks in results.multi_face_landmarks:
#                 self.mpDraw.draw_landmarks(
#                     image=output_image,
#                     landmark_list=face_landmarks,
#                     connections=self.MpFaceMesh.FACEMESH_TESSELATION,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_tesselation_style()
#                 )
#                 self.mpDraw.draw_landmarks(
#                     image=output_image,
#                     landmark_list=face_landmarks,
#                     connections=self.MpFaceMesh.FACEMESH_CONTOURS,
#                     landmark_drawing_spec=None,
#                     connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_contours_style()
#                 )
#         return output_image, results
    
#     def isOpen(self, image, face_mesh_results, face_part, threshold=5):
#         image_height, image_width, _ = image.shape
#         output_image = image.copy()
#         status = {}
#         if face_part == 'MOUTH':
#             INDEXES = self.MpFaceMesh.FACEMESH_LIPS
#         elif face_part == 'LEFT_EYE':
#             INDEXES = self.MpFaceMesh.FACEMESH_LEFT_EYE
#         elif face_part == 'RIGHT_EYE':
#             INDEXES = self.MpFaceMesh.FACEMESH_RIGHT_EYE
#         else:
#             return
#         for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
#             _, height, _ = self.getSize(image, face_landmarks, INDEXES)
#             _, face_height, _ = self.getSize(image, face_landmarks, self.MpFaceMesh.FACEMESH_FACE_OVAL)
#             if (height/face_height)*100 > threshold:
#                 status[face_no] = 'OPEN'
#             else:
#                 status[face_no] = 'CLOSE'
#                 color = (0, 0, 255)  # Red for closed

#             cv2.putText(output_image, f'FACE {face_no}: {status[face_no]}', (10, image_height-40), cv2.FONT_HERSHEY_PLAIN, 1.4, color, 2)
#         return output_image, status
    
#     def getSize(self, image, face_landmarks, INDEXES):
#         image_height, image_width, _ = image.shape
#         INDEXES_LIST = list(itertools.chain(*INDEXES))
#         landmarks = []
#         for INDEX in INDEXES_LIST:
#             landmarks.append((int(face_landmarks.landmark[INDEX].x * image_width), int(face_landmarks.landmark[INDEX].y * image_height)))
#             _,_, width, height = cv2.boundingRect(np.array(landmarks))
#             landmarks = np.array(landmarks)
#             return width, height, landmarks

#     def masking(self, image, filter_img, face_landmarks, face_part, INDEXES):
#         annotated_image = image.copy()
#         try:
#             filter_img_height, filter_img_width, _ =filter_img.shape
#             _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)             
#             required_height = int(face_part_height*2.5)     
#             resized_filter_img = cv2.resize(filter_img,     
#            (int(filter_img_width *                         
#            (required_height/filter_img_height)),            
#             required_height))                               
#             filter_img_height, filter_img_width, _ = resized_filter_img.shape
#             _, filter_img_mask = cv2.threshold( 
# 		cv2.cvtColor(resized_filter_img,          
#             	cv2.COLOR_BGR2GRAY), 25, 255,              
# 		cv2.THRESH_BINARY_INV) 
#             center = landmarks.mean(axis=0).astype("int") 
#         except Exception as e:
#             pass
        


import cv2
import numpy as np
import itertools
import mediapipe as mp

class FaceMesh():
    def __init__(self):
        self.mpFaceDetection = mp.solutions.face_detection
        self.face_detection = self.mpFaceDetection.FaceDetection(model_selection=0, min_detection_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.MpFaceMesh = mp.solutions.face_mesh
        self.faceMeshImages = self.MpFaceMesh.FaceMesh(static_image_mode=True, max_num_faces=2, min_detection_confidence=0.5)
        self.faceMeshVideos = self.MpFaceMesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.3)
        self.mpDrawStyles = mp.solutions.drawing_styles

    def detectFacialLandmarks(self, image, face_mesh):
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)  
        output_image = image.copy()
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(
                    image=output_image,
                    landmark_list=face_landmarks,
                    connections=self.MpFaceMesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_tesselation_style()
                )
                self.mpDraw.draw_landmarks(
                    image=output_image,
                    landmark_list=face_landmarks,
                    connections=self.MpFaceMesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mpDrawStyles.get_default_face_mesh_contours_style()
                )
        return output_image, results
    
    def isOpen(self, image, face_mesh_results, face_part, threshold=5):
        image_height, image_width, _ = image.shape
        output_image = image.copy()
        status = {}
        if face_part == 'MOUTH':
            INDEXES = self.MpFaceMesh.FACEMESH_LIPS
        elif face_part == 'LEFT_EYE':
            INDEXES = self.MpFaceMesh.FACEMESH_LEFT_EYE
        elif face_part == 'RIGHT_EYE':
            INDEXES = self.MpFaceMesh.FACEMESH_RIGHT_EYE
        else:
            return output_image, status
            
        for face_no, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            _, height, _ = self.getSize(image, face_landmarks, INDEXES)
            _, face_height, _ = self.getSize(image, face_landmarks, self.MpFaceMesh.FACEMESH_FACE_OVAL)
            
            # FIX: Ensure color is set for BOTH execution paths
            if (height/face_height)*100 > threshold:
                status[face_no] = 'OPEN'
                color = (0, 255, 0)  # Green for open
            else:
                status[face_no] = 'CLOSE'
                color = (0, 0, 255)  # Red for closed

            cv2.putText(output_image, f'FACE {face_no}: {status[face_no]}', (10, image_height-40), cv2.FONT_HERSHEY_PLAIN, 1.4, color, 2)
        return output_image, status
    
    def getSize(self, image, face_landmarks, INDEXES):
        image_height, image_width, _ = image.shape
        INDEXES_LIST = list(itertools.chain(*INDEXES))
        landmarks = []
        for INDEX in INDEXES_LIST:
            landmarks.append((int(face_landmarks.landmark[INDEX].x * image_width), int(face_landmarks.landmark[INDEX].y * image_height)))
            
        # FIX: The return statement must sit OUTSIDE the landmark collection loop
        landmarks = np.array(landmarks)
        _, _, width, height = cv2.boundingRect(landmarks)
        return width, height, landmarks

    def masking(self, image, filter_img, face_landmarks, face_part):
        if filter_img is None:
            return image
            
        if face_part == 'MOUTH':
            INDEXES = self.MpFaceMesh.FACEMESH_LIPS
        elif face_part == 'LEFT_EYE':
            INDEXES = self.MpFaceMesh.FACEMESH_LEFT_EYE
        elif face_part == 'RIGHT_EYE':
            INDEXES = self.MpFaceMesh.FACEMESH_RIGHT_EYE
        else:
            return image

        annotated_image = image.copy()
        try:
            # Handle both 3-channel and 4-channel transparent PNGs
            if len(filter_img.shape) == 3:
                filter_img_height, filter_img_width, _ = filter_img.shape
            else:
                filter_img_height, filter_img_width = filter_img.shape[:2]
                
            _, face_part_height, landmarks = self.getSize(image, face_landmarks, INDEXES)             
            
            # Adjust placement scales or offsets here if needed
            if face_part == 'MOUTH':
                required_height = int(face_part_height * 3.5) # Blown up larger for a grander flame effect
            else:
                required_height = int(face_part_height * 2.5)     
            
            if required_height <= 0 or filter_img_height <= 0:
                return image
                
            resized_filter_img = cv2.resize(filter_img, (int(filter_img_width * (required_height / filter_img_height)), required_height))                               
            
            if len(resized_filter_img.shape) == 3:
                h_f, w_f, _ = resized_filter_img.shape
            else:
                h_f, w_f = resized_filter_img.shape[:2]
                
            center = landmarks.mean(axis=0).astype("int") 
            
            # Calculate coordinates and position the animation down below the center of the mouth
            if face_part == 'MOUTH':
                x1 = int(center[0] - w_f / 2)
                y1 = int(center[1] - h_f / 4)  # Shifted downward so smoke trails outwards from lips
                x2 = x1 + w_f
                y2 = y1 + h_f
            else:
                x1 = int(center[0] - w_f / 2)
                y1 = int(center[1] - h_f / 2)
                x2 = x1 + w_f
                y2 = y1 + h_f
            
            # Dynamic screen clipping bounds
            h_img, w_img = image.shape[:2]
            x1_crop = max(0, x1)
            y1_crop = max(0, y1)
            x2_crop = min(w_img, x2)
            y2_crop = min(h_img, y2)
            
            # Calculate sub-region geometry for asset crop matching
            f_x1 = x1_crop - x1
            f_y1 = y1_crop - y1
            f_x2 = f_x1 + (x2_crop - x1_crop)
            f_y2 = f_y1 + (y2_crop - y1_crop)
            
            if (x2_crop - x1_crop) <= 0 or (y2_crop - y1_crop) <= 0:
                return image

            crop_filter = resized_filter_img[f_y1:f_y2, f_x1:f_x2]
            roi = annotated_image[y1_crop:y2_crop, x1_crop:x2_crop]
                
            # Transparent PNG configuration handling (Eyes)
            if crop_filter.shape[-1] == 4: 
                alpha = crop_filter[:, :, 3] / 255.0
                alpha = cv2.merge([alpha, alpha, alpha])
                foreground = crop_filter[:, :, :3]
                composite = cv2.convertScaleAbs(foreground * alpha + roi * (1.0 - alpha))
                annotated_image[y1_crop:y2_crop, x1_crop:x2_crop] = composite
            
            # Black Background Chroma screen-blend keying (Smoke MP4 Video)
            else: 
                gray_filter = cv2.cvtColor(crop_filter, cv2.COLOR_BGR2GRAY)
                # Adjust '15' lower if smoke is too invisible, or higher if box background leaks
                _, binary_mask = cv2.threshold(gray_filter, 15, 255, cv2.THRESH_BINARY)
                
                mask_inv = cv2.bitwise_not(binary_mask)
                bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
                fg = cv2.bitwise_and(crop_filter, crop_filter, mask=binary_mask)
                
                annotated_image[y1_crop:y2_crop, x1_crop:x2_crop] = cv2.add(bg, fg)
                
        except Exception as e:
            print("Masking error:", e)
            pass
            
        return annotated_image


