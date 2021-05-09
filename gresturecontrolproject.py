import cv2
import mediapipe as mp
import time
import HandTracker as ht
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# importing the module
import screen_brightness_control as sbc
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange=volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)
volume.SetMasterVolumeLevelScalar(50/100,None)
sbc.set_brightness(50)
minvol=volrange[0]
maxvol=volrange[1]

tipids=[4,8,12,16,20]

W,H=640,480
detector=ht.handDetector(detectionCon=0.7,maxHands=1)
cap=cv2.VideoCapture(0)
cap.set(3,W)
cap.set(4,H)
ini=np.interp(50,[10,200],[300,50])
volbar1,volbar2=300,300
area=0
v1,v=0,0
while True:
    sucess,img=cap.read()
    img=detector.findHands(img)
    lmlist,bbox=detector.findposition(img,draw=False)
    if len(lmlist)!=0:
        area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        #print(area)
        if(100<area<1000):
            fingers=detector.figerups(lmlist)
            #print(fingers)
            x1,y1=lmlist[4][1],lmlist[4][2]
            x2,y2=lmlist[8][1],lmlist[8][2]
            cx,cy=(x1+x2)//2 , (y1+y2)//2
            length=math.hypot(x2-x1,y2-y1)
            vol=np.interp(length,[10,200],[0,100])
            volbar=np.interp(length,[10,200],[300,50])
            smoothness=10
            vol=smoothness*round(vol/smoothness)
            countfinger=fingers.count(1)
            #print(length,vol)
            #print(countfinger)

            if(countfinger<=1):
                v1=vol
                volbar1=volbar
                volume.SetMasterVolumeLevelScalar(v1/100,None)
            if(countfinger>2):
                v=vol
                volbar2=volbar
                sbc.set_brightness(int(v))
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
            cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
            cv2.putText(img,f'Volume',(535,35),cv2.FONT_HERSHEY_COMPLEX,
                        0.6,(255,0,0),2)
            cv2.putText(img,f'Brightness',(10,35),cv2.FONT_HERSHEY_COMPLEX,
                        0.6,(255,0,0),2)
            cv2.rectangle(img,(bbox[0]-20,bbox[1]-20),(bbox[2]+20,bbox[3]+20),
                (0,255,0),2)
            
            cv2.rectangle(img,(40,50),(65,300),(255,0,0),2)
            cv2.rectangle(img,(40,int(volbar2)),(65,300),(255,0,0),cv2.FILLED)
            cv2.putText(img,f'{int(v)}%',(30,330),cv2.FONT_HERSHEY_COMPLEX,
                        0.6,(255,0,0),2)
            cv2.rectangle(img,(565,50),(590,300),(255,0,0),2)
            cv2.rectangle(img,(565,int(volbar1)),(590,300),(255,0,0),cv2.FILLED)
            cv2.putText(img,f'{int(v1)}%',(565,330),cv2.FONT_HERSHEY_COMPLEX,
                        0.6,(255,0,0),2)
            if length<30:
                cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
    if cv2.waitKey(100) & 0xff == ord('q'):
        break

    cv2.imshow("Image",img)
cap.release()
cv2.destroyAllWindows()