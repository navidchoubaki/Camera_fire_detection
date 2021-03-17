import cv2
import numpy as np
import playsound
import threading


fire_reported = 0
email_status = False
alarm_status = False

def play_audio():
    playsound.playsound("Alarm.mp3")
video = cv2.VideoCapture(0)
while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (1000,600))
    blur = cv2.GaussianBlur(frame, (15,15),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    lower = [22,50,50]
    upper = [35,255,255]
 
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')
    mask = cv2.inRange(hsv,lower,upper)
    output = cv2.bitwise_and(frame,hsv,mask=mask)
    number_of_total = cv2.countNonZero(mask)
    if int(number_of_total) > 2000:
        fire_reported = fire_reported +  1

    cv2.imshow("Result", output)

    if fire_reported >= 1:

        if alarm_status == False:
            threading.Thread( target=play_audio ).start()
            alarm_status = True

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
video.release()

