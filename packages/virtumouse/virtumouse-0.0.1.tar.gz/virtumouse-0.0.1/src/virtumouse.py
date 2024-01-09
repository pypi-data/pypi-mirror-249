# original:https://github.com/ytakefuji/mediapipe_hand/blob/main/fingerv0.py
# original is modified by kumada
\
import mediapipe as mp
import numpy as np
import pyautogui

import cv2
import math
import numpy as np
import threading

import sys

CLICK_ANGLE = 10    ## Angle to determine click status
CAMERA = 0          ## Capture camera number(cv2) default 0

class HandDetector:
    def __init__(self, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.hands = Hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidence,
                                   min_tracking_confidence=min_tracking_confidence)

    def findHandLandMarks(self, image, handNumber=0, draw=False):
        originalImage = image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # mediapipe needs RGB
        results = self.hands.process(image)
        landMarkList = []

        if results.multi_hand_landmarks:  # returns None if hand is not found
            hand = results.multi_hand_landmarks[handNumber] #results.multi_hand_landmarks returns landMarks for all the hands

            for id, landMark in enumerate(hand.landmark):
                # landMark holds x,y,z ratios of single landmark
                imgH, imgW, imgC = originalImage.shape  # height, width, channel for image
                xPos, yPos = int(landMark.x * imgW), int(landMark.y * imgH)
                landMarkList.append([xPos, yPos])

        return landMarkList


Hands = mp.solutions.hands
Draw = mp.solutions.drawing_utils
handDetector = HandDetector(min_detection_confidence=0.7)


def mouth_main():
 
  cam = cv2.VideoCapture(CAMERA)
  display_size = pyautogui.size()
  cam_size = [cam.get(cv2.CAP_PROP_FRAME_WIDTH) - 50, cam.get(cv2.CAP_PROP_FRAME_HEIGHT) - 50] # -の値をもたせることで余裕をもたせる寸法
  
  while True:
    
    status, image = cam.read()
    image =cv2.flip(image,1)
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=False) ## detect hand_landmarks
    pointer_state, pointer_pos = check_pointer(handLandmarks,cam_size)
    
    
    ## 画面内に入ったタイミングで処理開始
    if pointer_state == True:
    
        # click 処理
        lclick_state = check_clicked(handLandmarks)
        rclick_state = check_rclicked(handLandmarks)

        winposition = parse_window(pointer_pos, display_size, cam_size)
        pyautogui.moveTo(winposition[0], winposition[1])
        
        
        # print(winposition)
        if lclick_state == True:
            pyautogui.click(winposition[0],winposition[1])
        if rclick_state == True:
            pyautogui.rightClick(winposition[0],winposition[1])
        elif lclick_state == False and rclick_state == False:
            #pyautogui.mouseUp()
            pass



## L click_func
def check_clicked(handLandmarks):
    
    if(len(handLandmarks) != 0):
        
        index_tumb_angle = calc_angle(handLandmarks[8], handLandmarks[5], handLandmarks[4])
        
        ## 指定の角度が以下でクリック判定
        if index_tumb_angle < CLICK_ANGLE:
            return True
    else:
        return False


## R click_func
def check_rclicked(handLandmarks):
    if(len(handLandmarks) != 0):
        
        thumb_angle = calc_angle(handLandmarks[12], handLandmarks[9], handLandmarks[4])
        
        ## 指定の角度が以下でクリック判定
        if thumb_angle < CLICK_ANGLE:
            return True
    else:
        return False



## calc angle (I: 3positions / O: angle)
def calc_angle(pos1,pos2,pos3) -> float:
    vec1 = np.array(pos1) - np.array(pos2)
    vec2 = np.array(pos3) - np.array(pos2)
    
    cos_angle = np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    angle = math.degrees(math.acos(cos_angle))
    
    return angle


## 指先(pointer)が枠内に入っているかチェック
def check_pointer(handLandmarks,cap_size):
    ## 画面外ならfalse
    if(len(handLandmarks) != 0):
        ## 座標が- ならfalse
        if handLandmarks[8][0] < 0:
            return False, []
        if handLandmarks[8][1] < 0:
            return False, []
        ## 座標がカメラより先に出ているならfalse
        if handLandmarks[8][0] - cap_size[0]  > 0:
            return False, []
        if handLandmarks[8][1] - cap_size[1] > 0:
            return False, []

        ## 親指の指先
        return True ,handLandmarks[4]
    return False, []


## window画面に合わせる処理
def parse_window(xy:list, display_size, cam_size)->list:
    x_ = display_size[0]/cam_size[0] * xy[0] # x
    y_ = display_size[1]/cam_size[1] * xy[1] # y
    
    return [x_,y_]


## 実行処理
def main():
    thread = threading.Thread(target=mouth_main)
    thread.setDaemon(True) ## background
    thread.start()
    print("## if this app quit you input \"q\"")
    command = "Normal"
    while command.lower() != "q":
        command = input()


if __name__ == '__main__':
    main()