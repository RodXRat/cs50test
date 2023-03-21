import json
import os

CONFIG_DIR = "./config"
CONFIG_FILE = "{}/config.json".format(CONFIG_DIR)
OPENCV_DIR = "./OpenCV"

default_config = {
    "COMPORT": "COM3",
    "OPENCV_DIR": "./OpenCV",
    "GAME": "VAL3",
    "DEBUG": "0",
    "DEBUG2": "0",
    "KILL_SWITCH": "caps lock",
    "MOUSE_BUTTON_ENGAGE": "pynput.mouse.Button.x2",
    "DISPLAY": "True",
    "ACTIVATION_RANGE": "500",
    "MONITOR_FACTOR": "2",
    "CONFIDENCE_THRESHOLD": "0.55",
    "NMS_THRESHOLD": ".55",
    "TRIGGERZONE": "15",
    "BUFFERZONE": "15"
}


def read_config():
    with open(CONFIG_FILE, "r") as js:
        JSON_DATA = json.load(js)
    return JSON_DATA


def gen_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(default_config, f)
    return read_config()


def write_config(key, setting):
    js = open(CONFIG_FILE)
    JSON_DATA = json.load(js)
    js.close()
    JSON_DATA[key] = str(setting)
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(JSON_DATA, outfile)
    print(key + " " + JSON_DATA[key])
    print()


if (os.path.exists(CONFIG_DIR)):
    pass
else:
    os.mkdir(CONFIG_DIR)

if (os.path.exists(CONFIG_FILE)):
    JSON_DATA = read_config()
else:
    JSON_DATA = gen_config()


KILLSWITCH = False
ENGAGE = False
SHOOT = False

closestObject = []
lastMovement = 0
lastReset = 0
timeClick = 0
timeEngage = 0
difXLast, difYLast = 0, 0

LABELS = "{}/{}/classes.labels".format(
    JSON_DATA["OPENCV_DIR"], JSON_DATA["GAME"])
WEIGHTS = "{}/{}/yolov4.weights".format(
    JSON_DATA["OPENCV_DIR"], JSON_DATA["GAME"])
CONFIG = "{}/{}/yolov4.cfg".format(JSON_DATA["OPENCV_DIR"], JSON_DATA["GAME"])

COLORS = [(0, 255, 255), (255, 255, 0), (0, 255, 0), (255, 0, 0)]
AIMPOINT = int((int(JSON_DATA["ACTIVATION_RANGE"]) / 2))

BOX_X = 0
BOX_Y = 1
BOX_WIDTH = 2
BOX_HEIGHT = 3
BOX_CENTERX = 4
BOX_CENTERY = 5
BOX_CCLOSESTX = 6
BOX_CCLOSESTY = 7
BOX_DISTANCE = 8
BOX_CLASS = 9
BOX_HMOD = 10
