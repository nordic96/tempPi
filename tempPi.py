#!/usr/bin/python
# -*- coding:utf-8 =*-
import smbus
import time
import math
import datetime
import RPi.GPIO as GPIO

LED = 7 #pin 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(1)
record = 0.0
f = open('temprec.txt', 'w')
while True:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.5)
    bus.write_byte(address, A0)
    value = bus.read_byte(address)
    temp = (float)(value) * 33/255
    if record == temp:
        continue
    else:
        now = datetime.datetime.now()
        record = str(now) + ' Temp: %3.3f' %temp
        print record
        f.write(record + '\n')
        GPIO.output(LED, GPIO.LOW)
        time.sleep(1.5)
    record = temp
f.close()
