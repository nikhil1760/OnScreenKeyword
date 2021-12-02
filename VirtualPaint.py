import cv2,os,time,HandTrackingModule as htm
import numpy as np
folderPath = "C:/opencv/module2/project4/Header"
myList = os.listdir(folderPath)
brushThickness=15
eraseThickness=100
#print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
#print(len(overlayList))
header = overlayList[0]
print(header.shape)
cap=cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
drawColor=(255,0,255)
detector=htm.handDetector(detectionCon=0.85)
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),dtype=np.uint8)
while True:

    # 1. Import image
    success, img = cap.read()
    img=cv2.flip(img,1 )# to remove mirror problem (right to left conversion and vice versa)
    #2. Find Hand Landmarks
    img=detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]  # tip of index  finger
        x2, y2 = lmlist[12][1:]  # tip of  middle finger

        #3. Check which fingers are up
        fingers=detector.fingersup()
        #print(fingers)
        # 4. If Selection Mode – Two finger are up
        if fingers[1] and fingers[2]:
            #print("Selection mode")
            xp, yp = 0, 0
            if y1<125:
                if 120 < x1 < 300:
                    header = overlayList[1]
                    drawColor = (180,105,255)
                elif 300 < x1 < 530:
                    header = overlayList[2]
                    drawColor = (255, 0, 0)
                elif 530 < x1 < 720:
                    header = overlayList[3]
                    drawColor = (0, 255, 0)
                elif 720 < x1 < 950:
                    header = overlayList[4]
                    drawColor = (0, 0, 255)
                elif 950 < x1 < 1200:
                    header = overlayList[5]
                    drawColor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)


        # 5. If Drawing Mode – Index finger is up
        if fingers[1] and fingers[2]==False:
            print("Drwaing mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraseThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraseThickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp=x1,y1
    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY) # it convert gray image

    T,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV) # it creates the inverse image (color - black)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)

    img=cv2.bitwise_and(img,imgInv) # add images
    img=cv2.bitwise_or(img,imgCanvas) #add images

    img[0:125,0:1280]=header
    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5)  # it adds two images but brightness of color is lost
    cv2.imshow("image", img)
    cv2.waitKey(1)