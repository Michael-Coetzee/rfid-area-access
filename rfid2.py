import time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
from itertools import cycle
GPIO.setmode(GPIO.BCM)

GREEN_LED = 18
BLUE_LED = 24
RED_LED = 23
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

con = lite.connect('areaDatabase.db')       # link to database
cur = con.cursor()              # connect to DB

#create tables if they do not exist
cur.execute('CREATE TABLE IF NOT EXISTS employee (ID INTEGER PRIMARY KEY, Card TEXT, Name TEXT)') 
cur.execute('CREATE TABLE IF NOT EXISTS tracking (ID INTEGER PRIMARY KEY, Card TEXT, Date TEXT, Status INTERGER DEFAULT 0)')
cur.execute('CREATE TABLE IF NOT EXISTS rejected (ID INTEGER PRIMARY KEY, Card TEXT, Date TEXT)')

#============================================================================================================

cur.execute('REPLACE INTO employee values(0001, "121743110", "Deon Spengler")') #example code: remove when real world application
cur.execute('REPLACE INTO employee values(0002, "121723560", "Martin Heneck")') #example code: remove when real world application
cur.execute('REPLACE INTO employee values(0003, "121741279", "Francois Kotze")')#example code: remove when real world application

#============================================================================================================

GPIO.output(BLUE_LED, True)
try:
    while True:                             # loop until tag is read
        thetime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())
        rfid_data = raw_input().strip()                        # read data from rfid
        if  len(rfid_data) > 0:             # check data
            rfid_data = rfid_data[1:11]     # only get tag number
            print "Card Scanned. Tag ID:", rfid_data  # print number
            cur.execute("SELECT Name FROM employee WHERE Card = ?", [rfid_data])
            result = cur.fetchone()         # fetch name of card holder if exists
            if not result:                  # if card not found execute the following
                GPIO.output(BLUE_LED, False)
                GPIO.output(RED_LED, True)
                time.sleep(2)
                GPIO.output(RED_LED, False)
                GPIO.output(BLUE_LED, True)
                print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at area @ ",thetime
                cur.execute("INSERT INTO rejected (Card, Date) VALUES(?,?)", (rfid_data, thetime))
                con.commit()                # logging unauthorised card into database
                continue
            else:                           # if card found execute the following
                GPIO.output(BLUE_LED, False)
                GPIO.output(GREEN_LED, True)
                time.sleep(2)
                GPIO.output(GREEN_LED, False)
                GPIO.output(BLUE_LED, True)
                print "Card found in DB."
                print result[0],"entered area @",thetime
                cur.execute("SELECT Status FROM tracking WHERE Card = ?", [rfid_data])
                statusResult = cur.fetchone()
                if statusResult == (0,):
                    Entered = (1,)
                    print "Updating Enter"
                    cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, thetime, Entered))
                else:
                    print "Updating Exit"
                    Exited = (0,)
                    cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, thetime, Exited))
                    con.commit()
except KeyboardInterrupt:
    print "Caught interrupt, exiting..."
    print "Unexpected error:", sys.exc_info()[0]
    raise
finally:
    cur.close()
    GPIO.cleanup()                         # cleanup GPIO
