import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('lib_xml/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('lib_xml/haarcascade_eye.xml')
url = "rtsp://192.168.1.18:554/onvif1"
#cap = cv2.VideoCapture(url)
if 1:
	count = 0
        while True:
                #ret_val, img_raw = cap.read();
                #cv2.imshow('demo',img)
                cv2.namedWindow('img', cv2.WINDOW_NORMAL)
                img_raw= cv2.imread('d.jpg',0)
                cv2.imshow('img',img_raw)
                if(img_raw):
                    img = cv2.resize (img_raw, None, fx = 0.5, fy = 0.5)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(30, 30),
                        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
                    )
                    for (x,y,w,h) in faces:
                        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                        roi_gray = gray[y:y+h, x:x+w]
                        roi_color = img[y:y+h, x:x+w]
                        cv2.imwrite("tach/frame%d.jpg" % count, roi_color)  
                        eyes = eye_cascade.detectMultiScale(roi_gray)
                        for (ex,ey,ew,eh) in eyes:
                            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                    cv2.imshow('img',img)
                    cv2.imwrite("img/frame%d.jpg" % count, img)     # save frame as JPEG file
                    count+=1
                    print count
                    if cv2.waitKey(10) ==ord('q'):
                        break
                    if count ==20:
                        break
else:
        print ("camera open failed")

cv2.destroyAllWindows()

