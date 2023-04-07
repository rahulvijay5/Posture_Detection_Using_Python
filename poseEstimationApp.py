import cv2
import time
import poseEstimationModule as pm
import mediapipe as mp
mp_pose = mp.solutions.pose
import numpy as np
import os

folderPath = "images"
myList = os.listdir(folderPath)
print(myList)

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))

poseImage = overlayList[0]

# cap = cv2.VideoCapture('C:/Users/91897/Pictures/Camera Roll/temp2.mp4')
cap = cv2.VideoCapture(0)
cap.set(3,635)
cap.set(4,365)
imgBackground = overlayList[6]


cTime=0
pTime=0
detector = pm.poseDetector()
poseName = ""
while True:
    success, img = cap.read()

    

    # img = cv2.flip(img,1)
    img, img_novideo, pose_landmarks = detector.findPose(img, False)
    if pose_landmarks:
        landmarks = pose_landmarks.landmark
        # print(landmarks)
        # print("1: ", landmarks[0])
        # print(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
        
        # print(landmarks[12].x, landmarks[12].y)
        
        # getting angle between joints
        angle_12_24_26 = int(detector.calculate_angle([landmarks[12].x, landmarks[12].y], [landmarks[24].x, landmarks[24].y], [landmarks[26].x, landmarks[26].y]))
        angle_11_23_25 = int(detector.calculate_angle([landmarks[11].x, landmarks[11].y], [landmarks[23].x, landmarks[23].y], [landmarks[25].x, landmarks[25].y]))
        angle_14_12_24 = int(detector.calculate_angle([landmarks[14].x, landmarks[14].y], [landmarks[12].x, landmarks[12].y], [landmarks[24].x, landmarks[24].y]))
        angle_13_11_23 = int(detector.calculate_angle([landmarks[13].x, landmarks[13].y], [landmarks[11].x, landmarks[11].y], [landmarks[23].x, landmarks[23].y]))
        angle_16_14_12 = int(detector.calculate_angle([landmarks[16].x, landmarks[16].y], [landmarks[14].x, landmarks[14].y], [landmarks[12].x, landmarks[12].y]))
        angle_15_13_11 = int(detector.calculate_angle([landmarks[15].x, landmarks[15].y], [landmarks[13].x, landmarks[13].y], [landmarks[11].x, landmarks[11].y]))
        angle_24_26_28 = int(detector.calculate_angle([landmarks[24].x, landmarks[24].y], [landmarks[26].x, landmarks[26].y], [landmarks[28].x, landmarks[28].y]))
        angle_23_25_27 = int(detector.calculate_angle([landmarks[23].x, landmarks[23].y], [landmarks[25].x, landmarks[25].y], [landmarks[27].x, landmarks[27].y]))

        # cv2.putText(img, str(angle_24_26_28), 
        #                     tuple(np.multiply([landmarks[26].x, landmarks[26].y], [640, 480]).astype(int)), 
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        #                             )
        
        # cv2.putText(img, str(angle_23_25_27), 
        #                     tuple(np.multiply([landmarks[25].x, landmarks[25].y], [640, 480]).astype(int)), 
        #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
        #                             )


        # ---------Estimating pose-----------
        # 1. Mountain Pose
        poseImage = overlayList[5]
        if angle_24_26_28 > 150 and angle_23_25_27 > 150:       #waist_knees_ankle
            if angle_12_24_26 > 150 and angle_11_23_25 > 150:   #shoulder_waist_knees
                if angle_16_14_12 > 150 and angle_15_13_11 > 150:   #wrist_elbow_shoulder
                    if angle_14_12_24 < 30 and angle_13_11_23 < 30: #elbow_shoulder_waist
                        # poseName = "standing"
                        poseImage = overlayList[0]
                    elif angle_14_12_24 > 150 and angle_13_11_23 > 150:
                        # poseName = "armsUpPose"
                        poseImage = overlayList[1]
        # flag = 0
        if (angle_24_26_28 > 150 and angle_23_25_27 < 80) or (angle_24_26_28 < 80 and angle_23_25_27 > 150):
            # flag=1
            if (angle_12_24_26 > 150 and angle_11_23_25 in range(90,180)) or (angle_12_24_26 in range(90,180) and angle_11_23_25 > 150):
                # flag=2
                if angle_16_14_12 > 90 and angle_15_13_11 > 90:   #wrist_elbow_shoulder
                    # flag=3
                    if angle_14_12_24 > 120 and angle_13_11_23 > 120:
                        # flag=4
                        # poseName = "shivBhakt"
                        poseImage = overlayList[4]

        if angle_24_26_28 > 100 and angle_23_25_27 > 100:
            # flag=11
            if (angle_12_24_26 > 150 and angle_11_23_25 in range(80,130)) or (angle_12_24_26 in range(80,130) and angle_11_23_25 > 150):
                # flag=12
                if angle_16_14_12 > 130 and angle_15_13_11 > 130:   #wrist_elbow_shoulder
                    # flag=13
                    if angle_14_12_24 < 60 and angle_13_11_23 < 60:
                        # flag=14
                        # poseName = "oneLegUp"
                        poseImage = overlayList[3]

        if angle_24_26_28 > 120 and angle_23_25_27 > 120: 
            # flag = 21
            if angle_12_24_26 < 130 and angle_11_23_25 < 130:
                # flag=22
                if angle_14_12_24 in range(60,160) and angle_13_11_23 in range(60,160):
                    # flag=23
                    if angle_16_14_12 > 120 and angle_15_13_11 > 120:
                        # flag=24
                        # poseName = "frontBend"
                        poseImage = overlayList[2]

        # print(flag)
    # lmList = detector.findPosition(img, False)
    # print(lmList)
    # if len(lmList)!=0:
        # print(lmList)
        # track landmark 14 (right_elbow)
        # cv2.circle(img, (lmList[14][1],lmList[14][2]), 15, (0,0,255), cv2.FILLED)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # cv2.putText(img, str(int(fps)), (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
    # cv2.putText(img, poseName, (250,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    #camera video on top of background
    imgBackground[140:500,26:666] = img

    #Pose estimation picture on top of background
    imgBackground[140: 140+360,700:700+276] = poseImage

    cv2.imshow("Image", imgBackground)

    cv2.waitKey(1)
