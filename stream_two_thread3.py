import threading
import time
import Queue
import cv2
import numpy as np
import sys
import os
#---------------------Khai bao class---------------------
#tien trinh ham doc
class thread_read_img(threading.Thread):
    def __init__(self, name,cap):
        threading.Thread.__init__(self)
        self.name = name
        self.cap = cap
    def run(self):
        print "Bat dau doc camera ... " + self.name +"\n"
        read_img(self.cap)
        print "Ket thuc camera" + self.name +"\n"
#tien trinh nhan dien mat
class thread_seach_face(threading.Thread):
    def __init__(self,name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        print "Bat dau xu ly..." + self.name +"\n"
        seach_face(self.name)
        print "Ket thuc xu ly..." + self.name +"\n"

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
    global count
    if cap.isOpened():
        while exitFlag:
            if(img_queue.full()):
                img_queue.get()
            else:
                OK = cap.grab();
                if (OK == True):
                    ret_val, img_raw = cap.read()
                    print "read->ok"
                    img_queue.put(img_raw)

                    print "put->ok"
                else:
                    print "no reading camera!"
                    exitFalg = 0
	    
    else:
        print "camera open failed"
        exitFlag = 0
    cap.release()
    cv2.destroyAllWindows()
#ham seach face
def seach_face(name):
    global img_queue
    global img_queue_show
    global exitFlag
    global count
    face_cascade=cv2.CascadeClassifier('/home/tuan/Desktop/smarthome_cameraIP_FaceRecognition/lib_xml/haarcascade_frontalface_default.xml')
    while(exitFlag):
        Lock.acquire()
        if not img_queue.empty() and img_queue.qsize()>1:
            print "get..."
            img=img_queue.get()
            Lock.release()
            print "-> 0k"
            print name
            print "lay thanh cong!"
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
            Lock.acquire()
            if(img_queue_show.full()):
                print "---------"
            else:
                img_queue_show.put(img)
            Lock.release()
        else:
            Lock.release()
    cap.release()
    cv2.destroyAllWindows()
def show_img(threadName):
    global exitFlag
    global count
    global img_queue_show
    # Start time
    
    count =0
    kt=0
    while exitFlag:
        if cv2.waitKey(10)==ord('q'):
            end = time.time()
            tocdo=count/(end-start)
            print "toc do xu ly"
            print tocdo
            exitFlag=0
        if not img_queue_show.empty() and img_queue_show.qsize()>1:
            if kt==0:
                start = time.time()
                kt=1
            img_raw=img_queue_show.get()
            print "show"
            cv2.namedWindow( "Display window", cv2.WINDOW_NORMAL )
            img = cv2.resize (img_raw, None, fx = 0.5, fy = 0.5)
            cv2.imshow('Display window',img)
            count+=1
        else:
            pass
            #print "walting...\n"
            #print "size:%d"%(img_queue_show.qsize())
            #time.sleep(1)
#chuong trinh chinh
count =-100
exitFlag = 1      
img_queue = Queue.Queue(4)
img_queue_show = Queue.Queue(5)
Lock = threading.Lock()
ip=str(sys.argv[0])
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
url = "rtsp://10.1.17.83:554/onvif1"
cap = cv2.VideoCapture(url,cv2.CAP_FFMPEG)
if cap.isOpened():
    thread1 = thread_read_img("thread_read_img",cap)
    thread1.start()
    #------------------------
    thread2 = thread_seach_face("thread_seach_face ")
    thread2.start()
    #----------------------
    thread3 = thread_show_img("thread_show_img")
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
else:
    print "camera faile"
print "Ket thuc Main Thread" +"\n"
 






