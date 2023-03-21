import serial

from controls import *
from opencv import *
from screen import *


def start():

    arduino = serial.Serial(JSON_DATA["COMPORT"], 115200, timeout=0)

    mouse_listen()

    monitor, sct = get_monitor()
    model = get_model()
    return arduino, monitor, sct, model


def arduino_send(arduino, closestObject, triggerbot, difX, difY, timeNow, KILLSWITCH):
    lastMovement = timeNow

    difLoop = 2
    difXLoop = difX / difLoop
    difYLoop = difY / difLoop

    if difY < 2 and difY > -2:
        difYLoop = 0

    if KILLSWITCH == True:
        if int(JSON_DATA["DEBUG"]):
            print("Full")
            dataFull = str(difX) + ':' + str(difY) + ':' + str(triggerbot)
            print("Class: " +
                  str(closestObject[BOX_CLASS]) + " || Data: " + dataFull)
            print("Split")
        for x in range(math.trunc(difLoop + .9)):
            data = str(difXLoop) + ':' + str(difYLoop) + ':' + str(triggerbot)
            arduino.write(data.encode())
            if int(JSON_DATA["DEBUG"]):
                print("Class: " +
                      str(closestObject[BOX_CLASS]) + " || Data: " + data)
    else:
        data = str(difX) + ':' + str(difY) + ':' + str(triggerbot)
        if int(JSON_DATA["DEBUG"]):
            print("No Split")
            print("Class: " + str(closestObject[BOX_CLASS]) + " || Data: " + data)
        arduino.write(data.encode())
    print("Data:" + str(data))
    print("Class:" + str(closestObject[BOX_CLASS]))
    print("HMOD:" + str(closestObject[BOX_HMOD]))
    print("HEIGHT:" + str(closestObject[BOX_HEIGHT]))
    print()

    difXLast, difYLast = difX, difY
    return closestObject, lastMovement, difXLast, difYLast
