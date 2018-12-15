#!/usr/bin/python
# -*- coding:utf-8 =*-
import smbus
import time
import math
import datetime
import RPi.GPIO as GPIO
import MySQLdb


LED = 7 #pin 7
GREEN = 11
RED = 13
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.LOW)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)

address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43
bus = smbus.SMBus(1)
record = 0.0
f = open('temprec.txt', 'a')
db = MySQLdb.connect("localhost", "root", "nordic96", "test")

while True:
    cursor = db.cursor()
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(0.1)
    bus.write_byte(address, A0)
    value = bus.read_byte(address)
    temp = (float)(value) * 330/255
    if temp >= 31:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
    else:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)

    if record == temp:
        continue
    else:
        now = datetime.datetime.now()
        #mysql insertion
        sql = "insert into TempRecord(date, temp) values( %s, %s)"
        try:
            cursor.execute(sql, (now.strftime('%Y-%m-%d %H:%M:%S'), temp))
        except:
            db.rollback()
        db.commit()
        record = str(now) + ' Temp: %3.3f' %temp
        print record
        f.write(record + '\n')
        GPIO.output(LED, GPIO.LOW)
        time.sleep(600)
    record = temp
db.close()
f.close()
