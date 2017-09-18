from __future__ import print_function
import os
import glob
import sys
import MySQLdb
import spidev
import RPi.GPIO as GPIO
import datetime
from datetime import time
from time import sleep
import time
import subprocess

board_type = sys.argv[-1]

global temp
global soll
global now

soll = 17                       # Solltemperatur setzen!
raum = "1214"                   # Raumnummer setzen!

d = datetime
channels = [22, 18, 16, 15, 13, 11]
#           G25 G24 G23 G22 G27 G17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# setze Output der jeweiligen GPIO-Channel
i = 0
for pin in channels:
    if int(board_type) == 1 and i % 2 == 0:
        GPIO.setup(pin, GPIO.OUT)
    elif int(board_type) == 2 and i % 2 == 1:
         GPIO.setup(pin, GPIO.OUT)
    i = i + 1

GPIO.setup(7, GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,1)

def get_adc(channel):
        GPIO.output(7, GPIO.HIGH)
        GPIO.output(7, GPIO.LOW)
        if channel == 0:
                res = spi.xfer([1,128,0])
        elif channel == 1:
                res = spi.xfer([1,144,0])
        if 0 <= res[1] <= 3:
                return ((((res[1] * 256) + res[2]) * 0.00322) * 3)

def display(adc_temp):
    global datetime
    global temp
    temp = adc_temp * 5
    datetime = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:00"))
    print (time.strftime("%H:%M:%S",time.localtime()),';',"{0:04f}".format(adc_temp),';', temp)

def write_data_to_db(temp):
   print("writing data to DB...")
   try:
        conn = MySQLdb.connect(host="10.16.103.202",user="r1214",passwd="BGyPLrtGyVZG8Vyj",db="messung")
        cur = conn.cursor()
        sql = ("""INSERT INTO temp (room,temp,soll) VALUES (%s,%s,%s)""", (raum,round(temp, 1),round(soll, 1)))
        cur.execute(*sql)
        conn.commit()
        conn.close()
        print("write successful!")
   except:
        print("could not write data to DB")


sleep(60 * 5 * (int(board_type)-1) + 30)

while True:
    adc_temp = (get_adc(0))     # hole Rohdaten fuer Temperatur
    display(adc_temp)   # umrechnen der Rohdaten
    write_data_to_db(temp)  # schreibe Werte in Datenbank
