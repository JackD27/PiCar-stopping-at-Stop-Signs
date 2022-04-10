# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 19:36:33 2021

@author: Jackson
"""

class Stop:

    stop = False # Stop starts at False, we don't want to stop right away.
    number = 0 #Helps to stop the car by increasing the number.
    speed = 20 # Default speed it's set at.
 
    # Getters and Setters of the variables above.
    def setStop(self, n):
        self.stop = n
        
    def getStop(self):
        return self.stop
         
    def setNumber(self, n):
        self.number = n
        
    def getNumber(self):
        return self.number    
    
    def getSpeed(self):
        return self.speed
        
    def setSpeed(self, speed):
        self.speed = speed
