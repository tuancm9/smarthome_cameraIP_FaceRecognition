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
                print "waiting show img..."
                #print "hang doi%d \n"%(img_queue.qsize())
            else:
                OK = cap.grab();
                if (OK == True):
                    left = 0
                    right = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
                    if(right>10):
                        right=right-1
                    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,right)
                    ret_val, img_raw = cap.read()
                    count+=1
                    img_raw = cv2.resize (img_raw, None, fx = 0.3, fy = 0.3,interpolation =cv2.INTER_CUBIC)
                    img_queue.put(img_raw)
                    #time.sleep(1)
                else:
                    print "no reading camera!"
                    exitFalg = 0
            if count==10:
                break
	    
    else:
        print "camera open failed"
        exitFlag = 0
    cap.release()
    cv2.destroyAllWindows()
#ham seach face
face_cascade1 =cv2.CascadeClassifier('/home/pi/Desktop/stream/lib_xml/haarcascade_frontalface_default.xml')
face_cascade2=face_cascade3=face_cascade1
def seach_face(name):
    t1="thread_seach_face 1"
    t2="thread_seach_face 2"
    t3="thread_seach_face 3"
    if name==t1:
        global face_cascade1
        face_cascade=face_cascade1
    else:
        if name==t2:
            global face_cascade2
            face_cascade=face_cascade2
        else:
            if name==t3:
                global face_cascade3
                face_cascade=face_cascade3
            else:
                print "no"
    global img_queue
    global img_queue_show
    global exitFlag
    global count
    while(exitFlag):
        Lock.acquire()
        if not img_queue.empty() and img_queue.qsize()>1:
            img=img_queue.get()
            Lock.release()
            print name
            print "lay thanh cong!"
            imgg= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                    imgg,
                    scaleFactor=1.2,
                    minNeighbors=5
            )
            print "xly 1..."
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
        if count==10:
            break
    cap.release()
    cv2.destroyAllWindows()
def show_img(threadName):
    global exitFlag
    global count
    global img_queue_show
    while exitFlag:
        if cv2.waitKey(10)==ord('q'):
                exitFlag=0
        if not img_queue_show.empty() and img_queue_show.qsize()>2:

            img_raw=img_queue_show.get()
            cv2.namedWindow( "Display window", cv2.WINDOW_NORMAL )
	    img = cv2.resize (img_raw, None, fx = 0.3, fy = 0.3)
            cv2.imshow('Display window',img)
      
        #else:
            #print "walting...\n"
            #print "size:%d"%(img_queue_show.qsize())
            #time.sleep(1)
        if count ==10:
            break
#chuong trinh chinh
count =-100
exitFlag = 1      
img_queue = Queue.Queue(20)
img_queue_show = Queue.Queue(20)
Lock = threading.Lock()
ip=str(sys.argv[0])
url = "rtsp://192.168.1.18:554/onvif1"
cap = cv2.VideoCapture(url)
if cap.isOpened():
    thread1 = thread_read_img("thread_read_img",cap)
    thread1.start()
    #------------------------
    thread2 = thread_seach_face("thread_seach_face 1")
    thread2.start()
    thread4 = thread_seach_face("thread_seach_face 2")
    thread4.start()
    thread5 = thread_seach_face("thread_seach_face 3")
    thread5.start()
    #----------------------
    thread3 = thread_show_img("thread_show_img")
    thread3.start()
    thread1.join()
    thread2.join()
    thread3.join()
else:
    print "camera faile"
print "Ket thuc Main Thread" +"\n"
 






