import math
from microbit import *


def mapping(value, fromLow, fromHigh, toLow, toHigh):
    a = (toLow - toHigh) / (fromLow - fromHigh)
    b = toHigh - a * fromHigh
    exact = a * value + b
    rest = exact - math.floor(exact)
    if rest > 0.5:
        return math.ceil(exact)
    else:
        return math.floor(exact)

def flightcontrol(Throttle=0, Yaw=0, Pitch=0, Roll=0, Arm=0, flightMode=1, Buzzer=0):

    buf = bytearray(16)
    scaling = 1023/180
    offset = 512  # Header "Fade" (Spektsat code)
    buf[0] = 0  # Header "System" (Spektsat code)
    buf[1] = 0x01
    # 0x01 22MS 1024 DSM2
    # 0x12 11MS 2048 DSM2
    # 0xa2 22MS 2048 DSMS
    # 0xb2 11MS 2048 DSMX
    # Calibrate mode, perform a calibration of the acc using stick command
    if flightMode == 3:
        Throttle = 100
        Yaw = -90
        Pitch = -90
        Roll = 0
        Arm = 0
        flightMode = 1
    # Upscale Aux (Aux = true or false)
    Arm11 = 0
    if Arm == 0:
        Arm11 = 0
    if Arm == 1:
        Arm11 = 180 * scaling
    # Upscale Buzzer (Buzzer = 0 or 1)
    Buzzer11 = 0
    if Buzzer == 0:
        Buzzer11 = 0
    if Buzzer == 1:
        Buzzer11 = 180 * scaling
    # Acro mode (no self level)
    if flightMode == 0:
        flightMode = 0
    # Stabilise / self level mode
    if flightMode == 1:
        flightMode = 180
    # Vision mode similar to angle mode in terms of stabilisation in flight controller
    if flightMode == 2:
        flightMode = 180
    if Throttle > 100:
        Throttle = 100
    if Throttle < 0:
        Throttle = 0
    if Yaw > 90:
        Yaw = 90
    if Yaw < -90:
        Yaw = -90
    if Pitch > 90:
        Pitch = 90
    if Pitch < -90:
        Pitch = -90
    if Roll > 90:
        Roll = 90
    if Roll < -90:
        Roll = -90
    pitch11 = int(Pitch * scaling + offset)
    roll11 = int(Roll * scaling + offset)
    yaw11 = int(Yaw * (scaling) + offset)
    throttleS = int((Throttle * 1023) / 100)
 #   throttleS = 5
    flightMode11 = int(flightMode * scaling)
    buf[2] = (0 << 2) | ((roll11 >> 8) & 3)
    buf[3] = roll11 & 255
    buf[4] = (1 << 2) | ((pitch11 >> 8) & 3)
    buf[5] = pitch11 & 255
    buf[6] = (2 << 2) | ((throttleS >> 8) & 3)
    buf[7] = throttleS & 255
    buf[8] = (3 << 2) | ((yaw11 >> 8) & 3)
    buf[9] = yaw11 & 255
    buf[10] = (4 << 2) | ((int(Arm11) >> 8) & 3)
    buf[11] = int(Arm11) and int(255)
    buf[12] = (5 << 2) | ((flightMode11 >> 8) & 3)
    buf[13] = flightMode11 & 255
    buf[14] = (6 << 2) | ((Buzzer11 >> 8) & 3)
    buf[15] = Buzzer11 & 255
    uart.write(buf)
    
  
