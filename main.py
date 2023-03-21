import time
import numpy as np
import keyboard
import sys

from os import system

sys.path.insert(1, './import')
system("cls")

from utils import *
from triggerbot import *
from screen import *
from opencv import *
from controls import *
from config import *



## Program Start ##

arduino, monitor, sct, model = start()
print("Program Starting")
print()

run = False

## Program Loop ##
while True:
    start = time.time()

    ENGAGE, KILLSWITCH, SHOOT = check_keys()

    frame = np.array(grab_screen(region=monitor))
    classes, scores, boxes = do_detect(model, frame)
    enemyNum = len(boxes)
    hmod = 0

    if (enemyNum > 0):
        closestObject, run, data, difX, difY, triggerbot, new_bbox = cycle_enemies(run, enemyNum, frame, arduino, classes, boxes, closestObject)
        if ENGAGE:
            timeNow = time.time()
            timeResult = float(timeNow - lastMovement)
            zone = 4
            zone2 = 15
            zone3 = 1
            maxmove = 5
            x = difX - difXLast
            y = difY - difYLast
            if timeResult >= .075:
                closestObject, lastMovement, difXLast, difYLast = arduino_send(arduino, closestObject, triggerbot, difX, difY, timeNow, KILLSWITCH)
                run = False

            elif ((x >= zone2) or (x <= -zone2) or (y >= zone2) or (y <= -zone2)):
                if int(JSON_DATA["DEBUG2"]):
                    print("===== DONT MOVE =====")
                    print("== Too big, switch? ==")
                    print()
                pass

            elif ((x <= zone3) and (x >= -zone3) and (y <= zone3) and (y >= -zone3)):
                if int(JSON_DATA["DEBUG2"]):
                    print("===== DONT MOVE =====")
                    print("== Too small, relax ==")
                    print(x, y)
                    print()
                pass


            
            elif ( ( ((difX <= maxmove) and (difX >= -maxmove)) or ((x >= zone) or (x <= -zone)) ) and ( ((difY <= maxmove) and (difY >= -maxmove)) or ((y >= zone) or (y <= -zone)) )):
                closestObject, lastMovement, difXLast, difYLast = arduino_send(arduino, closestObject, triggerbot, difX, difY, timeNow, KILLSWITCH)
                run = False

            elif timeResult >= .025:
                run = False
                pass
        else:
            timeNow2 = time.time()
            timeResult2 = float(timeNow2 - lastReset)
            if timeResult2 > .025:
                lastReset = time.time()
                run = False
    do_display_start(classes, scores, boxes, frame, get_classes())
    end = time.time()
    do_display_end(start, end, frame)

    if (check_quit(sct)):
        print("Program Closing")
        break
             