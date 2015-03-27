""" Experiment with face detection and image filtering using OpenCV """

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
kernel = np.ones((21,21),'uint8')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20,20))
    for (x,y,w,h) in faces:
    	#frame[y:y+h,x:x+w,:] = cv2.dilate(frame[y:y+h,x:x+w,:], kernel)
    	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255))
    	cv2.circle(frame, (x+w/2, y+h/2), w/2, (0,255,255), -1)
    	cv2.circle(frame, (x+3*w/10, y+4*h/10), w/16, (0,0,0), -1)
    	cv2.circle(frame, (x+3*w/10+w/40, y+4*h/10-w/40), w/50, (255,255,255), -1)
    	cv2.circle(frame, (x+7*w/10, y+4*h/10), w/16, (0,0,0), -1)
    	cv2.circle(frame, (x+7*w/10-w/40, y+4*h/10-w/40), w/50, (255,255,255), -1)
    	nose = np.array([[x+w/2-w/80, y+h/2], [x+w/2+w/80, y+h/2], [x+w/2, y+h/2+w/80]], np.int32)
    	cv2.fillPoly(frame, [nose], (0,0,0))
    	cv2.ellipse(frame, (x+w/2-w/20, y+57*h/100), (w/20, w/30), 0, 0, 150, (0,0,0), 2)
    	cv2.ellipse(frame, (x+w/2+w/20, y+57*h/100), (w/20, w/30), 0, 30, 180, (0,0,0), 2)
    	cv2.circle(frame, (x+2*w/10, y+6*h/10), w/12, (0,0,255), -1)
    	cv2.circle(frame, (x+8*w/10, y+6*h/10), w/12, (0,0,255), -1)


    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()