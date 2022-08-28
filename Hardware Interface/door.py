from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)

def open () : 
    for i in range(35, -90, -5) : 
        servo.angle = i
        sleep(0.1)

def close() : 
    for i in range(-90, 35, 5) :
        servo.angle = i
        sleep(0.1)

