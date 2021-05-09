import cv2
import mediapipe as mp
import time
class handDetector():
    def __init__(self,mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands= mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
            imageRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results=self.hands.process(imageRGB)
            if self.results.multi_hand_landmarks:
                for hand in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img,hand,self.mpHands.HAND_CONNECTIONS)
            return img
    def thumb(self,lmlist): 
        if lmlist[4][1]>lmlist[4-1][1]:
            return True
        else:
            return False
    
    def figerups(self,lmlist):
        tipids=[8,12,16,20]
        fingers=[]
        for id in range(0,4):
            if lmlist[tipids[id]][2]<lmlist[tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    def findposition(self,img,handNo=0,draw=True):
        lmlist=[]
        xlist=[]
        ylist=[]
        bbox=[]
        if self.results.multi_hand_landmarks:
            myhand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myhand.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x * w),int(lm.y*h)
                xlist.append(cx)
                ylist.append(cy)
                
                lmlist.append([id,cx,cy])
            xmin,xmax=min(xlist),max(xlist)
            ymin,ymax=min(ylist),max(ylist)
            bbox=xmin,ymin,xmax,ymax
        return lmlist,bbox

def main():
    cap=cv2.VideoCapture(0)
    detector=handDetector()
    while True:
        sucess,img=cap.read()
        img=detector.findHands(img)
        lmlist=detector.findposition(img)    
        cv2.imshow("Image",img)
        cv2.waitKey(1)

if __name__=="__main__":
    main()
