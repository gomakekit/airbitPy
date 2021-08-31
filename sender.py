from microbit import *
import radio
import math
Throttle=0
Yaw=0
Arm = 0
RadioChannel = 7
radio.on()
radio.config(channel=RadioChannel,power=7)
display.scroll(RadioChannel)

def map(value,fromLow,fromHigh,toLow,toHigh):
    a=(toLow-toHigh)/(fromLow-fromHigh)
    b=toHigh-a*fromHigh
    exact=a*value+b
    rest=exact-math.floor(exact)
    if rest>0.5: return math.ceil(exact)
    else: return math.floor(exact)
    display.scroll("Py")
display.set_pixel(0,4,9)
while True:
    sleep(20)
    display.clear()
    display.set_pixel(2,0,9)    #Yaw indicator (not implemented yet)
    display.set_pixel(4,4,9)    #Battery indicator (not implemented yet)
    Roll=map(accelerometer.get_x(),-1023,1024,-90,90)
    if Roll>90: Roll=90
    if Roll<-90: Roll=-90
    Pitch=map(accelerometer.get_y(),-1023,1024,-90,90)
    if Pitch>90: Pitch=90
    if Pitch<-90: Pitch=-90
    if button_a.was_pressed() and button_b.was_pressed():
        if Arm == 0: Arm = 1 
        else: Arm = 0
    if button_a.was_pressed():  
        Throttle=Throttle-5             #Decrease throttle by 5%
    if button_b.was_pressed():     
        Throttle=Throttle+5             #Increase throttle by 5%
    if Throttle>100: Throttle=100
    if Throttle<0: Throttle=0
    if accelerometer.was_gesture("shake"):  #Panic button
        Throttle = 0
        Arm = 0    
    
    if Arm: display.set_pixel(0,0,9)    #Show arming indicator on display if armed
    
    display.set_pixel(0,map(Throttle,0,100,4,0),9)  #Show throttle indicator
    display.set_pixel(map(Roll,-90,90,0,4),map(Pitch,-90,90,0,4),9) #Show roll/pitch indicator
    sendTekst = str(Pitch)+","+str(Arm)+","+str(Roll)+","+str(Throttle)+","+str(Yaw)
    radio.send(sendTekst)
