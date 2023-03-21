
import cv2
import mss.tools
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from config import *

def get_monitor():
    with mss.mss() as sct:
        Wd, Hd = sct.monitors[1]["width"], sct.monitors[1]["height"]
        factor = float(JSON_DATA["MONITOR_FACTOR"])
        range = float(JSON_DATA["ACTIVATION_RANGE"])
        activation_range = int(range / 2)
        monitor = (x := int(Wd / factor - activation_range),
                   y := int(Hd / factor - activation_range),
                   int(Wd / factor + activation_range),
                   int(Hd / factor + activation_range))
    return monitor, sct


def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        widthScr = x2 - left + 1
        heightScr = y2 - top + 1
    else:
        widthScr = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        heightScr = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, widthScr, heightScr)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (widthScr, heightScr),
                 srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (heightScr, widthScr, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
