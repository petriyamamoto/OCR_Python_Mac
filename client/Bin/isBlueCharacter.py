import cv2
import numpy as np
import matplotlib.pyplot as plt

def isBlueCharacter(img):
    try:
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h = img2[:,:,0]
        hist_h = cv2.calcHist([h],[0],None,[256],[0,256])
        result = np.where(hist_h > np.amax(hist_h)/10)
        if (result[0] > 100).any():
            return True
        else: return False
    except: 
            print('BlueCharacter Function Exception')
            return False
# print(isBlueCharacter(cv2.imread('title3.png')))