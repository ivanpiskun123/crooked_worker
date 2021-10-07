# to create statistics folder and add images with date
from datetime import date, datetime
import os
import numpy as np
# image processing and eyes/face detection
import cv2
# to measure head (eyes line) skew angle
# and get module of eyes position difference (head skew calculation)
import math
# video input resolution options
from video_process.capture_options import set_resolution
# video width and hight
from video_process.resolution_params import *
# to make sound notification
from  sound_notify.sound_notify import call
# to measure incorrect position siting time in separate thread
import threading
import time
# wrong position and duration in it restriction constant
from restriction_constants.duration import *
from restriction_constants.position import *


def wrong_sit_notify():
    t = threading.currentThread()
    INCORECT_POSITION_DURATION_TIME = 0
    while not getattr(t, "stop", False):
        if getattr(t, "pause", False):
            continue

        # if on last frame emplyee was in incorrect position
        if getattr(t, "incorrect_pos", False):
            # add 1 second to INCORECT_POSITION_DURATION_TIME
            time.sleep(1)
            INCORECT_POSITION_DURATION_TIME += 1
            # if emplyee sits in incorrect position to long
            if INCORECT_POSITION_DURATION_TIME >= MAX_INCORECT_POSITION_DURATION_TIME:
                call()
                # save image in folder with current date
                if not os.path.exists("../STATISTICS/"+str(date.today())):
                    os.makedirs("../STATISTICS/"+str(date.today()))
                cv2.imwrite("../STATISTICS/{}/{}.jpg".format(str(date.today()),
                                datetime.now().strftime("%H:%M:%S").replace(":", "_")), getattr(t, "current_frame")
                                )
                print("../STATISTICS/{}/{}.jpg".format(str(date.today()),datetime.now().strftime("%H:%M:%S").replace(":", "_")))
                INCORECT_POSITION_DURATION_TIME = 0
        # if position of employee get straighten
        else:
            INCORECT_POSITION_DURATION_TIME = 0


def main():
    # downloaded from https://github.com/Itseez/opencv/blob/master/data/haarcascades/
    # load classifiers into variables
    face_cascade = cv2.CascadeClassifier('classifiers/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('classifiers/haarcascade_eye.xml')

    # set video input resolution
    cap = cv2.VideoCapture(0)
    cap = set_resolution(cap)

    # start waiting for long wrong siting encounter in separate Thread
    wrong_sit_duration = threading.Thread(target=wrong_sit_notify)
    wrong_sit_duration.start()

    # retrive frames and classify
    while 1:
        incorrect_sit_on_current_frame = False
        ret, img = cap.read()
        wrong_sit_duration.current_frame = img

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        # if emplyee sits in very bad pos and can't detect him at all
        # or if he left work place without stoping or pausing programm with 'p' or 's'
        if len(faces)==0:
            wrong_sit_duration.incorrect_pos = True
            incorrect_sit_on_current_frame = True

        for (x,y,w,h) in faces:
            # skip if it`s outside man accidentally walking in front of camera
            if h < MIN_FACE_HIEGHT_TO_PROCESS:
                continue

            # show face detection boundaries
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

            # process employee siting position checking with restriction boundaries
            if (
                x<LEFT_BOUND_X or x+w>RIGHT_BOUND_X
                or y+h>BOTTOM_BOUND_Y or h>MIN_DISTANCE_FROM_MONITOR
                or h<MAX_DISTANCE_FROM_MONITOR
                ):
                wrong_sit_duration.incorrect_pos = True
                incorrect_sit_on_current_frame = True

            eyes = eye_cascade.detectMultiScale(roi_gray)
            eyes_count = 0

            # eyes detection
            for (ex,ey,ew,eh) in eyes:
                eyes_count += 1
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            # process employee head position with head skew angle (relative eyes position)
            # if two eye in frame captured
            if eyes_count == 2 and (eyes[0][0]-eyes[1][0] )!=0 :
                if (math.degrees
                        (np.arctan(
                                math.fabs((eyes[0][1]-eyes[1][1]) / (eyes[0][0]-eyes[1][0] ))
                            )
                        ) > MAX_ALLOWABLE_ANGLE):
                    wrong_sit_duration.incorrect_pos = True
                    incorrect_sit_on_current_frame = True
            # if on current frame emplyee was sitting right
            if not incorrect_sit_on_current_frame:
                wrong_sit_duration.incorrect_pos = False


        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 113: # 'q'
            wrong_sit_duration.stop = True
            break
        if k == 112: # 'p'
            wrong_sit_duration.pause = True
            input("Press Enter to continue...") # press Enter in console to continue
            wrong_sit_duration.pause = False

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
