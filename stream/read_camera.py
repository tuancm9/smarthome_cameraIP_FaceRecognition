#!/usr/bin/env python
import threading
import time
import Queue
import cv2
import numpy as np
import sys
import os
img_queue = Queue.Queue(4)
Lock = threading.Lock()
exitFlag = 1
class thread_read_img(threading.Thread):
    def __init__(self, name,cap):
        threading.Thread.__init__(self)
        self.name = name
        self.cap = cap
    def run(self):
        print "Bat dau doc camera ... " + self.name +"\n"
        self.read_img(self.cap)
        print "Ket thuc camera" + self.name +"\n"
	def read_img(self,cap):
	    if cap.isOpened():
	        while self.exitFlag:
	            if(self.img_queue.full()):
	                self.img_queue.get()
	            else:
	                OK = self.cap.grab();
	                if (OK == True):
	                    ret_val, img_raw = self.cap.read()
	                    print "read->ok"
	                    self.img_queue.put(img_raw)

	                    print "put->ok"
	                else:
	                    print "no reading camera!"
	                    self.exitFlag = 0
		    
	    else:
	        print "camera open failed"
	        exitFlag = 0
	    cap.release()
	    cv2.destroyAllWindows()
	def get_img(self):
		self.Lock.acquire()
		if(img_queue.qsize()>1):
			img=self.img_queue.get()
			return True,img
		self.Lock.release()
		return False,None
	def set_exitFlag(self,exitFlag):
		self.exitFlag=exitFlag
	def get_exitFlag(self):
		return self.exitFlag