import cv2
import time
import os
import HandDetectionModule as htm
import mediapipe as mp
wCam,hCam=1040,900

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

folderPath = "resources"
myList=os.listdir(folderPath)
print(myList)
overlayList= []
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))
pTime=0

detector=htm.handDetector(detectionCon=0.5)
tipIds=[4,8,12,16,20]
while(True):
    success,img= cap.read()
    img = detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    # print(lmList)

    if len(lmList)!=0:
        fingers=[]
        # Thumb
        if lmList[tipIds[0]][2]<lmList[tipIds[1]-3][2]:
             fingers.append(1)
        else:
              fingers.append(0)
        # 4 Fingers
        for id in range(1,5):
          if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
             fingers.append(1)
          else:
              fingers.append(0)
        #print(fingers)
        totalFingers=fingers.count(1)
        print(totalFingers)
        img=cv2.flip(img,90)
        h,w,c=overlayList[totalFingers-1].shape
        img[0:h, 0:w] = overlayList[totalFingers-1]
        cv2.rectangle(img,(20,420),(170,600),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,550),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),24)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img, f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
