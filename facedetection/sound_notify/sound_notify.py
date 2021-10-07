# sound notification making
import winsound
# sound params
from  sound_notify.sound_params import *

def call():
    winsound.Beep(FREQ, DURATION)
