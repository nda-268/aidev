# import cv2
# import numpy as np
# import time
# import os
# import HandTrackingModule as htm

# detector = htm.HandDetector(detectionCon=0.85)

# cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1080)
# myListDirectory = os.listdir("Meeting 19/header")
# print(myListDirectory)
# overlayList = []

# for imPath in myListDirectory:
#     image = cv2.imread(f'Meeting 19/header/{imPath}')
#     overlayList.append(image)

# header = overlayList[0]
# drawColor = (0, 0, 255)
# brushThickness = 7
# eraserThickness = 40
# xp, yp = 0, 0
# imgCanvas = np.zeros((1080, 1920, 3), np.uint8)

# while True:
#     res, frame = cap.read()
#     frame=cv2.flip(frame, 1)
#     frame = detector.findHands(frame)
#     lmList = detector.findPosition(frame, draw=True)
#     if len(lmList) != 0:
#         x1, y1 = lmList[8][1:]
#         x2, y2 = lmList[12][1:]
#         # print(x1, y1, x2, y2)
#         fingers = detector.fingersUp()
#         # print(fingers)
#         if fingers[1] and fingers[2]:
#             xp, yp = 0,0
#             print("Selection Mode")
#             cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
#             if y1 < 125:
#                 if 320 < x1 < 480:
#                     header = overlayList[0]
#                     drawColor = (0, 0, 255)
#                 elif 480 < x1 < 630:
#                     header = overlayList[1]
#                     drawColor = (0, 255, 0)
#                 elif 630 < x1 < 840:
#                     header = overlayList[2]
#                     drawColor = (255,0,0)
#                 elif x1> 1000:
#                     header = overlayList[3]
#                     drawColor = (0,0,0)  # eraser mode = black color
#         if fingers[1] and fingers[2] == False:
#             print("Drawing Mode")
#             cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
#             if xp == 0 and yp == 0:
#                 xp, yp = x1, y1
#             if drawColor == (0, 0, 0):
#                 cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
#             else:
#                 cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)
#                 cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
#             xp, yp = x1, y1
# # 1. Resize imgCanvas to match the width and height of frame
# # frame.shape returns (height, width, channels), but cv2.resize needs (width, height)
#     imgCanvas = cv2.resize(imgCanvas, (frame.shape[1], frame.shape[0]))

# # 2. Process your masks
#     frameGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
#     _, frameInvers = cv2.threshold(frameGray, 50, 255, cv2.THRESH_BINARY_INV)
#     frameInvers = cv2.cvtColor(frameInvers, cv2.COLOR_GRAY2BGR)

# # 3. Combine the layers (this will now succeed)
#     frame = cv2.bitwise_and(frame, frameInvers)
#     frame = cv2.bitwise_or(frame, imgCanvas)

#     frame[0:125, 0:1280] = header
#     frame = cv2.resize(frame, (1920, 1080))
#     imgCanvas = cv2.resize(imgCanvas, (1920, 1080))
#     cv2.imshow("Video Frame", frame)
#     cv2.imshow("Canvas", imgCanvas)
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import os
import HandTrackingModule as htm

detector = htm.HandDetector(detectionCon=0.85)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Detect the precise hardware boundaries
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Actual Camera Resolution: {width}x{height}")

myListDirectory = os.listdir("Meeting 19/header")
overlayList = []

for imPath in myListDirectory:
    image = cv2.imread(f'Meeting 19/header/{imPath}')
    # Match your graphic elements perfectly to your real camera layout
    image = cv2.resize(image, (width, 125)) 
    overlayList.append(image)

header = overlayList[0]
drawColor = (0, 0, 255)
brushThickness = 7
eraserThickness = 40
xp, yp = 0, 0

imgCanvas = np.zeros((height, width, 3), np.uint8)

# --- NEW: Setup responsive, monitor-friendly display windows ---
cv2.namedWindow("Video Frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("Canvas", cv2.WINDOW_NORMAL)

# Fit comfortably on your 1080p screen by scaling the display slightly lower
cv2.resizeWindow("Video Frame", 1280, 720)
cv2.resizeWindow("Canvas", 1280, 720)

while True:
    res, frame = cap.read()
    if not res:
        break
        
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame, draw=True)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        fingers = detector.fingersUp()
        
        # Selection Mode
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection Mode")
            cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
            
            if y1 < 125:
                # Dynamically split the interface based on real camera dimensions
                if (width * 0.16) < x1 < (width * 0.25):   # Roughly 320 to 480 at 1920p
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                elif (width * 0.25) < x1 < (width * 0.33): # Roughly 480 to 630 at 1920p
                    header = overlayList[1]
                    drawColor = (0, 255, 0)
                elif (width * 0.33) < x1 < (width * 0.44): # Roughly 630 to 840 at 1920p
                    header = overlayList[2]
                    drawColor = (255, 0, 0)
                elif x1 > (width * 0.52):                  # Roughly over 1000 at 1920p
                    header = overlayList[3]
                    drawColor = (0, 0, 0)  
                    
        # Drawing Mode
        if fingers[1] and not fingers[2]:
            print("Drawing Mode")
            cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
                
            if drawColor == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(frame, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1
            
    frameGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, frameInvers = cv2.threshold(frameGray, 50, 255, cv2.THRESH_BINARY_INV)
    frameInvers = cv2.cvtColor(frameInvers, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, frameInvers)
    frame = cv2.bitwise_or(frame, imgCanvas)

    # Apply header across entire real layout width
    frame[0:125, 0:width] = header
    
    cv2.imshow("Video Frame", frame)
    cv2.imshow("Canvas", imgCanvas)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
