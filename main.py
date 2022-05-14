import Motors
import numpy as np
import controller
import RPi.GPIO as GPIO          
from time import sleep
import VL53L0X
import VL53L0X_example
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os
#set the default pwm value to start with
pwmL=Motors.pwmValueStart(60)
pwmR=Motors.pwmValueStart(60)

tof = VL53L0X.VL53L0X(i2c_bus=1,i2c_address=0x29)
tof1 = VL53L0X.VL53L0X(i2c_bus=3,i2c_address=0x29)

tof.open()
tof1.open()

tof.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)
tof1.start_ranging(VL53L0X.Vl53l0xAccuracyMode.BETTER)


def moveBackward():
    Motors.motorS()
    sleep(0.01)
    while True:
        dl=tof1.get_distance()/10
        dr=tof.get_distance()/10
        print(dl , dr)
    
        if dr<51 and dl<51:
            Motors.motorB(25)
            print('moving backward')
        else:
            
            Motors.motorS()
            
            #stop untill the object infront moves again
            if dr>55 or dl> 5:
                pwmL=40
                pwmR=40
                break
        sleep(0.01)

while True:
    dl=tof1.get_distance()/10
    dr=tof.get_distance()/10
    
    print(dl , dr)
    
    #stop and movebackword to d=50 cm when d gets less than 5 ==> object stopped
    if dr<5 and dl<5:
        moveBackward()
    else:
        `
        [pwmChangeL, pwmChangeR]=controller.control(dl,dr)
        
        #print('pwm Left change is: '+str(pwmChangeL))
        #print('pwm right change is: '+str(pwmChangeL))
        
        if pwmL<=40 and pwmChangeL>0:
            pwmL=pwmL+pwmChangeL
        elif pwmL>=90 and pwmChangeL<0:
            pwmL=pwmL+pwmChangeL
        elif pwmL>40 and pwmL<90:
            pwmL=pwmL+pwmChangeL
        else:
            pass
        
        if pwmR<=40 and pwmChangeR>0:
            pwmR=pwmR+pwmChangeR
        elif pwmR>=90 and pwmChangeR<0:
            pwmR=pwmR+pwmChangeR
        elif pwmR>40 and pwmR<90:
            pwmR=pwmR+pwmChangeR
        else:
            pass       
        print('new Left pwm is   : '+str(pwmL))
        print('new Left pwm is   : '+str(pwmR))
        
        Motors.motors(pwmL,pwmL)
        
        
        print('sleep for 0.5 sec')
        sleep(0.1)
        


tof.stop_ranging()
tof.close()
tof1.stop_ranging()
tof1.close()
