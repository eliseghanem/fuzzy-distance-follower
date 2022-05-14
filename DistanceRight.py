import time
import busio
import board
import adafruit_vl53l0x
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

i2c = busio.I2C(3, 2)
vl53=adafruit_vl53l0x.VL53L0X(i2c)

def getDistance():
    return float(vl53.range/10)
print(vl53.range/10)