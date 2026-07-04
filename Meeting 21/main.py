import cv2
import mediapipe as mp
import math
from math   import hypot
print(math.hypot(3, 4))  

cap = cv2.VideoCapture(0)
nose_img = cv2.imread(r"C:/Users/nda/Documents/GitHub/aidev/Meeting 21/pig_nose.png", cv2.IMREAD_UNCHANGED)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mpDraw = mp.solutions.drawing_utils
mpDrawingStyles = mp.solutions.drawing_styles
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=4)

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", 1280, 720) # Or any size that fits your screen nicely

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(rgb)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # mpDraw.draw_landmarks(
            #     image=frame,
            #     landmark_list=face_landmarks,
            #     connections=mpFaceMesh.FACEMESH_TESSELATION,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mpDrawingStyles.get_default_face_mesh_tesselation_style()
            # )
            # mpDraw.draw_landmarks(
            #     image=frame,
            #     landmark_list=face_landmarks,
            #     connections=mpFaceMesh.FACEMESH_CONTOURS,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mpDrawingStyles.get_default_face_mesh_contours_style()
            # )
            leftnosex = 0
            leftnosey = 0
            rightnosex = 0
            rightnosey = 0
            centernosex = 0
            centernosey = 0
            for lm_id, lm in enumerate(face_landmarks.landmark):
                h, w, c = rgb.shape
                x, y = int(lm.x * w), int(lm.y * h)
                if lm_id == 49:
                    leftnosex, leftnosey = x, y
                if lm_id == 279:
                    rightnosex, rightnosey = x, y  
                if lm_id == 5:
                    centernosex, centernosey = x, y
            nose_width = int(hypot(rightnosex - leftnosex, rightnosey - leftnosey) * 1.2)
            nose_height = int(nose_width * 0.8)
            # if (nose_width and nose_height)!= 0:
            #     pig_nose = cv2.resize(nose_img, (nose_width, nose_height))
            # top_left = (int(centernosex - nose_width / 2), int(centernosey-nose_height / 2))
            # bottom_right = (int(centernosex + nose_width / 2), int(centernosey + nose_height / 2))
            # nose_area = frame[top_left[1]:top_left[1]+nose_height, top_left[0]:top_left[0]+nose_width]
            # pig_nose_gray = cv2.cvtColor(pig_nose, cv2.COLOR_BGR2GRAY)
            # _, nose_mask = cv2.threshold(pig_nose_gray, 25, 255, cv2.THRESH_BINARY_INV)
            # no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
            # final_nose = cv2.add(no_nose, pig_nose)
            # frame[top_left[1]:top_left[1]+nose_height, top_left[0]:top_left[0]+nose_width] = final_nose
            if (nose_width and nose_height) != 0:
                # 1. Resize the original transparent image
                pig_nose_resized = cv2.resize(nose_img, (nose_width, nose_height))
                
                # 2. Safely calculate coordinates and slice the exact area
                top_left_x = int(centernosex - nose_width / 2)
                top_left_y = int(centernosey - nose_height / 2)
                
                # Prevent crashing if the nose goes off the edge of the screen
                if top_left_y >= 0 and top_left_x >= 0 and (top_left_y + nose_height) <= h and (top_left_x + nose_width) <= w:
                    nose_area = frame[top_left_y : top_left_y + nose_height, top_left_x : top_left_x + nose_width]
                    
                    # 3. Extract the alpha channel (channel 3) to use as a mask
                    if pig_nose_resized.shape[2] == 4:
                        alpha_channel = pig_nose_resized[:, :, 3]
                        _, nose_mask = cv2.threshold(alpha_channel, 25, 255, cv2.THRESH_BINARY_INV)
                        # Drop alpha channel so it becomes 3-channel BGR
                        pig_nose = cv2.cvtColor(pig_nose_resized, cv2.COLOR_BGRA2BGR)
                    else:
                        # Fallback if image doesn't have transparency
                        pig_nose_gray = cv2.cvtColor(pig_nose_resized, cv2.COLOR_BGR2GRAY)
                        _, nose_mask = cv2.threshold(pig_nose_gray, 25, 255, cv2.THRESH_BINARY_INV)
                        pig_nose = pig_nose_resized

                    # 4. Combine them safely (shapes now match perfectly)
                    no_nose = cv2.bitwise_and(nose_area, nose_area, mask=nose_mask)
                    
                    # Create the opposite mask to isolate the pig nose pixels
                    pig_mask_inv = cv2.bitwise_not(nose_mask)
                    pig_nose_isolated = cv2.bitwise_and(pig_nose, pig_nose, mask=pig_mask_inv)
                    
                    final_nose = cv2.add(no_nose, pig_nose_isolated)
                    frame[top_left_y : top_left_y + nose_height, top_left_x : top_left_x + nose_width] = final_nose
    cv2.imshow("Frame", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

