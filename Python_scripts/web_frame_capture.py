import cv2
import os
from datetime import datetime
import time

cwd = os.getcwd()

while(1):

    vid1 = cv2.VideoCapture("http://50.246.145.122:80/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER")
    vid2 = cv2.VideoCapture("http://96.56.250.139:8200/mjpg/video.mjpg")
    vid3 = cv2.VideoCapture("http://220.157.160.198:8080/-wvhttp-01-/GetOneShot?image_size=640x480&frame_count=1000000000")

    dateTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    ret, frame =  vid1.read()
    if(ret):
        cv2.imwrite(f'{cwd}/test_images/feed1/{dateTime}.jpg',frame)

    ret, frame =  vid2.read()
    if(ret):
        cv2.imwrite(f'{cwd}/test_images/feed2/{dateTime}.jpg',frame)

    ret, frame =  vid3.read()
    if(ret):
        cv2.imwrite(f'{cwd}/test_images/feed3/{dateTime}.jpg',frame)

    time.sleep(3600)
