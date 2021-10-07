# import video resolution params to make
# restricting boundaries relative from resolution
from video_process.resolution_params import *

# captured as min and max size of employee head in image frame
# head y-dimension
MIN_DISTANCE_FROM_MONITOR=HEIGHT/2 # to close
MAX_DISTANCE_FROM_MONITOR=HEIGHT/4 # to far

# left, right, bottom boundaries
LEFT_BOUND_X = WIDTH/5 # bent too far to the left
RIGHT_BOUND_X = WIDTH - WIDTH/5 # bent too far to the right
BOTTOM_BOUND_Y = HEIGHT-HEIGHT/5 # bent too far down

# head skew, maximum allowable angle 30 degrees,
# measured in degrees
MAX_ALLOWABLE_ANGLE = 15

# if someone walks or just appear beind employee
# hes face processin must be skipped
# that man can be recognized by significantly smaller
# face size because of his far distance from monitor and camera
MIN_FACE_HIEGHT_TO_PROCESS = HEIGHT/6
