# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 22:56:22 2021

@author: Jackson
"""
# PiCar CSC 485 Robotics Project!
import time
import cv2
import numpy as np
import threading
from stop import Stop
import picar
from picar.SunFounder_PCA9685 import Servo

startCode = False #To start the while loop

S = Stop() #Object frrom my start class

vid = cv2.VideoCapture(0) #Captures the video

# All PiCar settings that were used
fw = picar.front_wheels.Front_Wheels()
bw = picar.back_wheels.Back_Wheels()
pan_servo = Servo.Servo(1)
tilt_servo = Servo.Servo(2)
fw.offset = 0
fw.turn(90)
pan_servo.offset = 0
tilt_servo.offset = 0
bw.speed = 0
pan_servo.write(90)
tilt_servo.write(120)

#HSV Ranges
l_r1 = np.array([151, 52, 145]) # Lower level HSV values
u_r1 = np.array([255, 255, 255]) # Upper level HSV value in 

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt) # gets area of the contours.
        peri = cv2.arcLength(cnt, True) 
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True) # This approxmimate curves, Thank you Youtube!
        x, y, w, h = cv2.boundingRect(approx)
        if area > 10000 and len(approx) == 8: #Area is high, so, it's close and make sure it has 8 sides. It it does draw lines/text.
            #print(area)
            #cv2.rectangle(imgContour , (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            cv2.putText(imgContour, "Stop Sign", (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            return True # returns True for the getStop() method.
 
def startTimer(): # Uses timed threading for my stop and continue methods. S.getNumber() will be set back to 0 after 10 seconds. 
     if S.getStop() == True:
        S.setNumber(S.getNumber() + 1)
        if S.getNumber() == 1:
            print("Stopping Car")
            S.setSpeed(0)
            t = threading.Timer(5.0, lambda: continueSpeed()) # Car stop for 5 seconds, I also had to use youtube and google for lambda
            t.start()
            f = threading.Timer(10.0, lambda: setZero())
            f.start()
            
def continueSpeed(): # Sets speed back to 20
   S.setSpeed(20)
   print("Returning Speed back to ", S.getSpeed())

def setZero(): #Sets getNumber() value back to zero, to refresh the stop at a sign method.
    print("Set the getNumber() to zero successfully!")
    S.setNumber(0)
      
def Video(): # Captures the video and goes through different algorithms like canny and masking.
    startTimer()
    ret, frames = vid.read()
    
    imgContour = frames.copy()
    
    gaussian = cv2.GaussianBlur(frames, (7, 7), 1)
    grey = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(gaussian, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, l_r1, u_r1)
    canny = cv2.Canny(grey, 0, 48)
    
    # Will return True if the area > 10000 or approx == 8
    stop = getContours(canny, imgContour) 
    S.setStop(stop)
    
    bw.speed = S.getSpeed()
    bw.backward() #bw.backward() is forward for my PiCar, I may have put the motors on backwards. Idk...
    
    #Cosmetic stuff for appearance.
    if S.getSpeed() == 0:
        cv2.putText(imgContour, "STOP", (25, 37), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 255), 2)
    else:
        cv2.putText(imgContour, "GO!", (25, 37), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 2)
    if np.sum(mask1) > 4000000:
        cv2.putText(imgContour, "Mask Sum: " + str(np.sum(mask1)), (10, 420), cv2.FONT_HERSHEY_COMPLEX, 0.6, (80, 127, 255), 1)
    else:
        cv2.putText(imgContour, "Mask Sum: " + str(np.sum(mask1)), (10, 420), cv2.FONT_HERSHEY_COMPLEX, 0.6, (120, 255, 0), 1)
        
    #Shows the images.    
    cv2.imshow("Canny Detection", canny)
    cv2.putText(imgContour, "Speed: " + str(S.getSpeed()), (10, 450), cv2.FONT_HERSHEY_COMPLEX, 0.6, (120, 255, 0), 1)
    cv2.imshow("Car Camera", imgContour)
    cv2.imshow("HSV/Masking", mask1)
    
# Ask a question to start the while loop to run.    
answer = input("Start robot? yes or no.")
if answer == "yes":
    print("Running robot.")
    startCode = True
    bw.speed = 0
else:
    answer = input("Start robot? yes or no.")

#Starts the main code.
while(startCode):
    
    #I used threading here to start it, so I can run the other code to stop for 5 seconds. Threading helped a lot.
    threadVid = threading.Thread(target=Video())
    threadVid.start()
    
    # Press 'Q' to stop the code.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        threadVid.join()
        print("Stopping Robot")
        break
 
#To end everything, like the video, backwheels stop moving, camera back in place etc. After while loop breaks.    
fw.offset = 0
pan_servo.offset = 30
tilt_servo.offset = 0  
bw.stop()
cv2.destroyAllWindows()
vid.release()


