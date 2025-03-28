import cv2
import mediapipe as mp
import pyautogui
from pyautogui import click
cap = cv2.VideoCapture(0) #acces webcam
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width , screen_height = pyautogui.size()
index_y = 0 #store coordinate of index finger
while True:
    _, frame = cap.read() #read frame from live video
    frame = cv2.flip(frame ,1) #flip frame horizontal
    frame_height, frame_width, _= frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand) #drwa hand landmarks
            landmarks= hand.landmark #get landmark position
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                if id== 8: #index finger tip
                    cv2.circle(img =frame, center=(x,y), radius=10,color=(0,255,255)) #draw circle
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_x,index_y) #move the mouse cursor
                if id== 4: #thumb tip
                    cv2.circle(img =frame, center=(x,y), radius=10,color=(0,255,255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    print('outside', abs(index_y - thumb_y)) #print distance b/w index and thumb finger
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click() #mouse click
                        pyautogui.sleep(1) #delay to avoid multiple clicks
    cv2.imshow('Virtual Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break