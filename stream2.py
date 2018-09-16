import cv2
import numpy as np
url = "rtsp://192.168.1.5:554/onvif1"
cap = cv2.VideoCapture(url)
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203,23,252)
if cap.isOpened():
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
	count=0
        while True:
                ret_val, img_raw = cap.read();
                #img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('demo',img)
                img_raw = cv2.imread('c.jpg')
                img = cv2.resize (img, None, fx = 0.3, fy = 0.3)
                #cv2.putText(img, "Name: Tuan", (60,60), fontface, fontscale, fontcolor ,2)
                cv2.imshow('img',img)
                count+=1
                print count
                
                if cv2.waitKey(1)==ord('q'):
                    break;   
else:
        print ("camera open failed")
cap.release()
cv2.destroyAllWindows()


