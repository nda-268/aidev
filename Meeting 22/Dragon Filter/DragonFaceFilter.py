# import cv2
# import FaceMeshDetector as fmd
# detector = fmd.FaceMesh()

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# left_eye = cv2.imread(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/left_eye.png", cv2.IMREAD_UNCHANGED)
# right_eye = cv2.imread(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/right_eye.png", cv2.IMREAD_UNCHANGED)
# smoke_animation = cv2.VideoCapture(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/smoke_animation.mp4")
# smoke_frame_counter = 0

# cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Frame", 1280, 720) 

# while True:
#     ret, frame = cap.read()
#     ret, smoke_frame = smoke_animation.read()
#     smoke_frame_counter += 1
#     if smoke_frame_counter == smoke_animation.get(cv2.CAP_PROP_FRAME_COUNT):
#         smoke_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         smoke_frame_counter = 0
#     frame = cv2.flip(frame, 1)
#     frame_face_mesh, face_mesh_results = detector.detectFacialLandmarks(frame, detector.faceMeshVideos)
#     cv2.imshow('Frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import FaceMeshDetector as fmd
# detector = fmd.FaceMesh()

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# left_eye = cv2.imread(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/left_eye.png", cv2.IMREAD_UNCHANGED)
# right_eye = cv2.imread(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/right_eye.png", cv2.IMREAD_UNCHANGED)
# smoke_animation = cv2.VideoCapture(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/smoke_animation.mp4")
# smoke_frame_counter = 0

# cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Frame", 1280, 720) 

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
        
#     ret_smoke, smoke_frame = smoke_animation.read()
#     smoke_frame_counter += 1
    
#     # Safely loop the smoke video if it runs out of frames
#     if not ret_smoke or smoke_frame_counter >= smoke_animation.get(cv2.CAP_PROP_FRAME_COUNT):
#         smoke_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)
#         smoke_frame_counter = 0
#         _, smoke_frame = smoke_animation.read()
        
#     frame = cv2.flip(frame, 1)
    
#     # Process face mesh
#     frame_face_mesh, face_mesh_results = detector.detectFacialLandmarks(frame, detector.faceMeshVideos)
    
#     if face_mesh_results.multi_face_landmarks:
#         mouth_frame, mouth_status = detector.isOpen(frame, face_mesh_results, 'MOUTH', threshold=15)
#         left_eye_frame, left_eye_status = detector.isOpen(frame, face_mesh_results, 'LEFT_EYE', threshold=4.5)
#         right_eye_frame, right_eye_status = detector.isOpen(frame, face_mesh_results, 'RIGHT_EYE', threshold=4.5)
#         for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
#             if left_eye_status[face_num] == 'OPEN':
#                 frame = detector.masking(frame, left_eye, face_landmarks, 'LEFT_EYE')
#             if right_eye_status[face_num] == 'OPEN':
#                 frame = detector.masking(frame, right_eye, face_landmarks, 'RIGHT_EYE')
#             if mouth_status[face_num] == 'OPEN':
#                 frame = detector.masking(frame, smoke_frame, face_landmarks, 'MOUTH')

#     # FIX: Display the frame containing the drawn face landmarks!
#     cv2.imshow('Frame', frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# smoke_animation.release() # Added to properly free memory
# cv2.destroyAllWindows()



import cv2
import FaceMeshDetector as fmd
detector = fmd.FaceMesh()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
left_eye = cv2.imread(r"Meeting 22/Dragon Filter/image/eye1.png", cv2.IMREAD_UNCHANGED)
right_eye = cv2.imread(r"Meeting 22/Dragon Filter/image/eye2.png", cv2.IMREAD_UNCHANGED)
smoke_animation = cv2.VideoCapture(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 22/Dragon Filter/image/smoke_animation.mp4")
smoke_frame_counter = 0

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", 1280, 720) 

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    ret_smoke, smoke_frame = smoke_animation.read()
    smoke_frame_counter += 1
    
    if not ret_smoke or smoke_frame_counter >= smoke_animation.get(cv2.CAP_PROP_FRAME_COUNT):
        smoke_animation.set(cv2.CAP_PROP_POS_FRAMES, 0)
        smoke_frame_counter = 0
        _, smoke_frame = smoke_animation.read()
        
    frame = cv2.flip(frame, 1)
    
    # Process face mesh coordinates
    frame_face_mesh, face_mesh_results = detector.detectFacialLandmarks(frame, detector.faceMeshVideos)
    
    if face_mesh_results.multi_face_landmarks:
        # Check components
        _, mouth_status = detector.isOpen(frame, face_mesh_results, 'MOUTH', threshold=15)
        _, left_eye_status = detector.isOpen(frame, face_mesh_results, 'LEFT_EYE', threshold=4.5)
        _, right_eye_status = detector.isOpen(frame, face_mesh_results, 'RIGHT_EYE', threshold=4.5)
        
        for face_num, face_landmarks in enumerate(face_mesh_results.multi_face_landmarks):
            if left_eye_status.get(face_num) == 'OPEN':
                frame_face_mesh = detector.masking(frame_face_mesh, left_eye, face_landmarks, 'LEFT_EYE')
            if right_eye_status.get(face_num) == 'OPEN':
                frame_face_mesh = detector.masking(frame_face_mesh, right_eye, face_landmarks, 'RIGHT_EYE')
            if mouth_status.get(face_num) == 'OPEN':
                frame_face_mesh = detector.masking(frame_face_mesh, smoke_frame, face_landmarks, 'MOUTH')

    # Display the fully modified frame mesh containing overlays
    cv2.imshow('Frame', frame_face_mesh)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
smoke_animation.release()
cv2.destroyAllWindows()
