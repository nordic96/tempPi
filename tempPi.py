#!/usr/bin/python
# -*- coding:utf-8 =*-
import smbus
import time
import math
from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
import MySQLdb
import lcd_16x2 as LCD
import buzzer

start = datetime.now()

def tempcheck(temp):
    if temp >= 31:
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
    else:
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)

def dbInsertValidate(now, startTime, timegap):
    if now >= startTime + timedelta(seconds=timegap):
        #mysql insertion
        sql = "insert into TempRecord(rec_year, rec_month, rec_date, rec_time, temp) values(%s, %s, %s, %s, %s)"
        # print sql %(now.year, now.month, now.day, now.strftime('%H:%M:%S'), temp)
        try:
            cursor.execute(sql, (int(now.year), int(now.month), int(now.day), now.strftime('%H:%M:%S'), temp))
            LCD.lcd_string('**db inserted**', 2)
            print '**temp value inserted**'
            buzzer.buzz(1)
        except:
            LCD.lcd_string('**db error!**', 2)
            time.sleep(2)
            db.rollback()
        db.commit()
        global start
        start = now


if __name__=='__main__':
    LED = 4 #pin 7/GPIO 4
    GREEN = 17
    RED = 27
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
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
    #f = open('temprec.txt', 'a')
    db = MySQLdb.connect("localhost", "root", "nordic96", "test")

    #init lcd screen
    LCD.lcd_init()


    try:
        while True:
            cursor = db.cursor()
            GPIO.output(LED, GPIO.HIGH)
            time.sleep(0.1)
            bus.write_byte(address, A0)
            value = bus.read_byte(address)
            temp = (float)(value) * 330/255
            tempcheck(temp)

            if record == temp:
                continue
            else:
                buzzer.buzz(0.1)
                now = datetime.now()

                dbInsertValidate(now, start, 10)

                record = str(now) + ' Temp: %3.3f' %temp
                LCD.lcd_string('Temp: %3.2f C' %temp, 1)
                LCD.lcd_string('Time: %s' %now.strftime('%H:%M:%S'), 2)
                print record
                GPIO.output(LED, GPIO.LOW)
                time.sleep(2)
            record = temp
    except KeyboardInterrupt:
        pass
    finally:
        db.close()
        GPIO.cleanup()
