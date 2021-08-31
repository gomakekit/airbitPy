# Write your code here :-)
from microbit import *
import airpymodule
import radio
# import math
Roll = 0
Pitch = 0
Throttle = 0
Yaw = 0
Arm = 0
RadioChannel = 7
radio.on()
radio.config(channel=RadioChannel,power=7)
display.scroll(RadioChannel)
uart.init(baudrate=115200, bits=8, parity=None, stop=1, tx=pin1, rx=pin2)


    
while True:
    sleep(20)
    display.clear()
    mottatt = radio.receive()                   #Receive radio P,A,R,T,Y values
    if mottatt:
        verdier = mottatt.split(",")            #Split into array
        Pitch = int(verdier[0])
        Arm = int(verdier[1])
        Roll = int(verdier[2])
        Throttle = int(verdier[3])
        Yaw = int(verdier[4])
        
    display.set_pixel(                          #Plot roll and pitch
        airpymodule.mapping(Roll, -90, 90, 0, 4),
        airpymodule.mapping(Pitch, -90, 90, 0, 4),
        9,
    )
    display.set_pixel(0, airpymodule.mapping(Throttle, 0, 100, 4, 0), 9)    #Plot throttle
    display.set_pixel(2, 0, 9)                  #Plot Yaw, dummy only (yet)
    display.set_pixel(4, 4, 9)                  #Plot battery, dummy only (yet)
    airpymodule.flightcontrol(Throttle, Yaw, -Pitch, Roll, Arm, 1, 0)
    

    
    
	