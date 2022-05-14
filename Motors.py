import RPi.GPIO as GPIO          
from time import sleep

# turn off channel warnings messages
GPIO.setwarnings(False)

in1 = 26
in2 = 16
in3 = 5
in4= 6
en = 20
en2=21
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

#initialize the outputs
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(en,1000)
p2=GPIO.PWM(en2,1000)

def pwmValueStart(pwm):
    p1.start(pwm)
    p2.start(pwm)
    return pwm

def motorF(pwm):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    p1.ChangeDutyCycle(pwm)
    p2.ChangeDutyCycle(pwm)

def motorB(pwm):
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    p1.ChangeDutyCycle(pwm)
    p2.ChangeDutyCycle(pwm)

def motors(pwm1,pwm2):
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    p1.ChangeDutyCycle(pwm1)
    p2.ChangeDutyCycle(pwm2)
    

def motorS():
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    

    
def main():
    pwmValueStart(25)
    motorF(25)
    sleep(1)
    motorF(50)
    sleep(1)
    motorF(75)
    sleep(1)
    motorS()
    sleep(1)
    motorB(25)
    sleep(1)
    motorB(50)
    sleep(1)
    motorB(75)
    sleep(1)
    motorS()
if __name__ == '__main__':
    pwmValueStart(25)
    #motorF(50)
    #sleep(1)
    #motorF(60)
    #sleep(1)
    #motorF(70)
    #sleep(1)
    motorS()
    #sleep(1)
    #motorB(70)
    #sleep(1)
    #motorB(40)
    #sleep(1)
    #motorS()