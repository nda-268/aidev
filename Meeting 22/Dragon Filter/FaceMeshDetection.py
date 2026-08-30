import cv2
import mediapipe

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
mp_face_mesh = mediapipe.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", 1280, 720) # Or any size that fits your screen nicely

def plot_landmarks(frame, facial_area_obj):
    for source_idx, target_idx in facial_area_obj:
        source = landmarks.landmark[source_idx]
        target = landmarks.landmark[target_idx]
        relative_source = (int(frame.shape[1] * source.x), int(frame.shape[0] * source.y))
        relative_target = (int(frame.shape[1] * target.x), int(frame.shape[0] * target.y))
        cv2.line(frame, relative_source, relative_target, (0, 255, 0), 2)

while True:
    ret, frame = cap.read()
    results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    landmarks = results.multi_face_landmarks[0]
    plot_landmarks(frame,mp_face_mesh.FACEMESH_CONTOURS)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
