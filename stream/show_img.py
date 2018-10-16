#!/usr/bin/env python
import threading
import time
import Queue
import cv2
import numpy as np
import sys
import o
from seach_img import get_exitFlag2,set_exitFlag2,get_img_show
#tien trinh hien thi hinh anh
class thread_show_img(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print "Bat dau xu ly..." + self.name +"\n"
        show_img(self.name)
        print "Ket thuc xu ly..." + self.name +"\n"
    def show_img(threadName):
	    count =0
	    kt=0
	    while self.get_exitFlag2():
	        if cv2.waitKey(10)==ord('q'):
	            end = time.time()
	            tocdo=count/(end-start)
	            print "toc do xu ly"
	            print tocdo
	            self.set_exitFlag2(0)
	        kt2,img=self.get_img_show()
	        if kt2:
	            if kt==0:
	                start = time.time()
	                kt=1
	            cv2.namedWindow( "Display window", cv2.WINDOW_NORMAL )
	            img = cv2.resize (img, None, fx = 0.3, fy = 0.3)
	            cv2.imshow('Display window',img)
	            count+=1
	        else:
	            pass
	            #print "walting...\n"
	            #print "size:%d"%(img_queue_show.qsize())
	            #time.sleep(1)