#!/usr/bin/env python
import threading
import time
import Queue
import cv2
import numpy as np
import sys
import os
import read_camera
img_queue_show = Queue.Queue(4)
Lock = threading.Lock()
#tien trinh nhan dien mat
class thread_seach_face(threading.Thread,read_camera):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print "Bat dau xu ly..." + self.name +"\n"
        seach_face(self.name)
        print "Ket thuc xu ly..." + self.name +"\n"
	def get_exitFlag2(self):
		rt=self.get_exitFlag()
		return rt

	def get_img_show(self):
		self.Lock.acquire()
		if(img_queue_show.qsize()>1):
			img=self.img_queue_show.get()
			return True,img
		self.Lock.release()
		return False,None
	def set_exitFlag2(exit):
		rt=self.get_exitFlag()
		return rt
    def seach_face(self):
	    face_cascade=cv2.CascadeClassifier('/home/tuan/Desktop/smarthome_cameraIP_FaceRecognition/lib_xml/haarcascade_frontalface_default.xml')
	    while(self.get_exitFlag()):
	        kt,img=self.get_img()
	        if kt:
	            gray= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	            print "xly 1..."
	            faces = face_cascade.detectMultiScale(
	                    gray,
	                    scaleFactor=1.3,
	                    minNeighbors=5
	            )
	            print "...>ok"
	            for (x,y,w,h) in faces:
	                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	                    #cv2.imwrite("tach/frame%d.jpg" % count, roi_color) 
	            print "xly 2..."
	            self.Lock.acquire()
	            if(self.img_queue_show.full()):
	                print "---------"
	            else:
	                self.img_queue_show.put(img)
	            self.Lock.release()
	    cv2.destroyAllWindows()