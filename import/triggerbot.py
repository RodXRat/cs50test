import math
import pynput
import pynput.mouse
from opencv import *
from config import *


def do_triggerbot(closestObject):

    result = math.hypot(closestObject[BOX_CCLOSESTX] - AIMPOINT, closestObject[BOX_CCLOSESTY] - AIMPOINT)

    if (result < int(JSON_DATA["TRIGGERZONE"])):
        trigger = 1
    else:
        trigger = 0
    
    return trigger
