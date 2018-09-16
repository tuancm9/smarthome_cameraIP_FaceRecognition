# -*- coding: utf8 -*-
import threading
import time
import Queue
import cv2
import numpy as np
import sys
#---------------------Khai bao class---------------------
#tien trinh ham doc
class thread_read_img(threading.Thread):
    def __init__(self, name,cap):
        threading.Thread.__init__(self)
        self.name = name
        self.cap = cap
    def run(self):
        print "Bắt dau doc camera ... " + self.name +"\n"
        read_img(self.cap)
        print "Ket thuc camera" + self.name +"\n"
#tien trinh hien thi hinh anh
class thread_show_img(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print "Bat dau xu ly..." + self.name +"\n"
        show_img(self.name)
        print "Ket thuc xu ly..." + self.name +"\n"
#---------------------Khai bao ham---------------------
def read_img(cap):
    global img_queue
    global exitFlag
    if cap.isOpened():
	count=0
        while exitFlag:
            if(img_queue.full()):
                print "waiting show img..."
                print "hang doi%d \n"%(img_queue.qsize())
            else:
                OK = cap.grab();
                if (OK == True):
                    ret_val, img_raw = cap.read()
                    img_queue.put(img_raw)
                else:
                    print "no reading camera!"
                    exitFalg = 0
	    
    else:
        print "camera open failed"
        exitFlag = 0
    cap.release()
    cv2.destroyAllWindows()
def show_img(threadName):
    count=1
    global exitFlag
    global img_queue
    while exitFlag:
        if cv2.waitKey(1)==ord('q'):
                exitFlag=0
        if not img_queue.empty() and img_queue.qsize()>5:
            img_raw=img_queue.get()
            cv2.namedWindow( "Display window", cv2.WINDOW_NORMAL )
	    img = cv2.resize (img_raw, None, fx = 0.3, fy = 0.3)
            cv2.imshow('Display window',img)
            count+=1
            print count
            if (count == 100):
                count = 1
        else:
            print "walting...\n"
            print "size:%d"%(img_queue.qsize())
            #time.sleep(1)
#chuong trinh chinh	
exitFlag = 1      
img_queue = Queue.Queue(20)
if(len(sys.argv)==2):
    ip=sys.argv[1]
else:
    print "tham so truyen vao: name.py + ip"
    sys.exit()
url = "rtsp://"+str(ip)+":554/onvif1"
cap = cv2.VideoCapture(url)
if cap.isOpened():
    thread1 = thread_read_img("thread_read_img",cap)
    thread1.start()
    time.sleep(0.1)
    thread2 = thread_show_img("thread_show_img")
    thread2.start()
else:
    print "camera faile"
print "Ket thuc Main Thread" +"\n"
 






