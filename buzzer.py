import RPi.GPIO as GPIO
import time

BuzzerPin = 26 #GPIO26

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.output(BuzzerPin, GPIO.LOW)

def buzz(sec):
    setup()
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(sec)
    GPIO.output(BuzzerPin, GPIO.LOW)

if __name__=='__main__':
    setup()
    while True:
        GPIO.output(BuzzerPin, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(BuzzerPin, GPIO.LOW)
        time.sleep(0.5)
