import cv2  #openCV is library for image processing
import mediapipe as mp #for pose estimation
import time
import numpy as np


class poseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.modelComplexity=modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode,self.modelComplexity,self.upBody,self.smooth, self.detectionCon,self.trackCon)

    def findPose(self, img, draw=True):
        img_novideo = cv2.convertScaleAbs(img, alpha=0, beta=0)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB.flags.writeable = False
        self.results = self.pose.process(imgRGB)
        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
                self.mpDraw.draw_landmarks(img_novideo, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        
        return img, img_novideo, self.results.pose_landmarks

    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape   #height,width,channel
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)
            
        return lmList
    
    def calculate_angle(self,a,b,c):
        a = np.array(a) # First
        b = np.array(b) # Mid
        c = np.array(c) # End
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        # print_radians = np.arctan2(c[1]-b[1], c[0]-b[0])
        # print_angle = np.abs(print_radians*180.0/np.pi)
        # print("angle between  wrist and elbow: ", print_angle)
        angle = np.abs(radians*180.0/np.pi)
        
        if angle >180.0:
            angle = 360-angle
            
        return angle


# def main():
#     cap = cv2.VideoCapture('C:/Users/91897/Pictures/Camera Roll/temp.mp4')
#     cTime=0
#     pTime=0
#     detector = poseDetector()
#     while True:
#         success, img = cap.read()
#         detector.findPose(img)
#         lmList = detector.findPosition(img)
#         if len(lmList)!=0:
#             print(lmList)
#             cv2.circle(img, (lmList[14][1],lmList[14][2]), 15, (0,0,255), cv2.FILLED)
        
#         cTime = time.time()
#         fps = 1/(cTime-pTime)
#         pTime = cTime

#         cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,0), 3)
#         cv2.imshow("Image", img)

#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()