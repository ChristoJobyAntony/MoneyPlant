import stepperMotor
import RPi.GPIO as GPIO

stepperMotor.run(+40)

GPIO.cleanup()

