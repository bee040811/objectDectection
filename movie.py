#!/usr/bin/env python
from cv2 import __version__
import numpy as np
import cv2,cv
import sys
import inspect

class video:
    def read(self):
        #cap = cv2.VideoCapture(filename)
        cap = cv2.VideoCapture(0)
        fgbg = cv2.BackgroundSubtractorMOG()
        count = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame,False)

            # threshhold classified 2 cluster
            ret,thresh = cv2.threshold(fgmask,127,255,0)
            row, col= thresh.shape
            # find contours
            contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame,contours,-1,(0,255,0),3)
            # find boundary (simple method)
            self._findBoundary( np.where((fgmask != 0)),frame )
            cv2.imshow('frame',frame)
            count += 1
            # rough adative change background 
            if count > 10:
                fgbg = cv2.BackgroundSubtractorMOG()
                count =0
            # wait key click Q or ESC to leave 
            if cv2.waitKey(30) & 0xFF == ord('q') or cv2.waitKey(30) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyWindow('frame')
    def _findBoundary(self,feature,frame):
        row,col ,chan = frame.shape
        minX = row
        minY = col
        maxX = 0
        maxY = 0
        print feature[0]
        print feature[1]
        print "\n"
        for i in range(0,len(feature[0])):
            y = feature[0][i]
            x = feature[1][i]

            if minX > x :
                minX = x
            elif maxX < x :
                maxX = x
            elif minY > y :
                minY = y
            elif maxY < y:
                maxY = y
        cv2.rectangle(  frame,
            (minX,minY),
            (maxX,maxY),
            (0,255,0),
            2
        )

    def _pixelValue(self, pixel,value):
        for i in range(0,2):
            if pixel[i] != value[i]:
                return 0
        return 1
if __name__ == "__main__":
    v = video()
    v.read()
