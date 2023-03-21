import pynput
from win32api import GetKeyState
from win32con import VK_CAPITAL

from config import *

## Mouse Listener ##
def mouse_listen():
    listener = pynput.mouse.Listener(on_click=on_click)
    listener.start()

## Mouse Callback ##
def on_click(x, y, button, pressed):
    global ENGAGE
    global SHOOT

    if pressed:
        if button == eval(JSON_DATA["MOUSE_BUTTON_ENGAGE"]):
            ENGAGE = True
        elif button == eval("pynput.mouse.Button.left"):
            SHOOT = True

    else:
        if button == eval(JSON_DATA["MOUSE_BUTTON_ENGAGE"]):
            ENGAGE = False
        elif  button == eval("pynput.mouse.Button.left"):
            SHOOT = False


## Keyboard Inputs ##
def check_keys():

    global KILLSWITCH
    global ENGAGE
    global SHOOT

    ## KILLSWITCH ##
    if (GetKeyState(VK_CAPITAL) == 1):
        KILLSWITCH = True
    else:
        KILLSWITCH = False

    return ENGAGE, KILLSWITCH, SHOOT
