#!/usr/bin/env python
import threading
import time
import Queue
import cv2
import numpy as np
import sys
import os
import read_camera,seach_face,show_img
if __name__ == '__main__':
    count =-100
    exitFlag = 1      
    ip=str(sys.argv[0])
    os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
    url = "rtsp://192.168.1.102:554/onvif1"
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
 