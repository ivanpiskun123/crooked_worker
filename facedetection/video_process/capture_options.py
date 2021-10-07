from video_process.resolution_params import *

def set_resolution(cap):
    cap.set(3, WIDTH) # 3 - 3th param in cap.set in width
    cap.set(4, HEIGHT) # 4 - 4th is height
    return cap
