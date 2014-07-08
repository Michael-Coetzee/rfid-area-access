import serial, time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GREEN_LED = 18
BLUE_LED = 24
RED_LED = 23
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

con = lite.connect('areaDatabase.db')       # link to database

rfid_reader = "/dev/ttyUSB0"                # link to usb port
print "Connected to RFID:"

GPIO.output(BLUE_LED, True)
try:
    while True:                             # loop until tag is read
        thetime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())
        rfid_data = raw_input().strip()     # read data from rfid
        if  len(rfid_data) > 0:             # check data
            rfid_data = rfid_data[1:11]     # only get tag number
            print "Card Scanned. Tag ID:", rfid_data  # print number
            cur = con.cursor()              # connect to DB
            cur.execute("select name from rfid where card = ?", [rfid_data])
            result = cur.fetchone()         # fetch name of card holder if exists
            if not result:                  # if card not found execute the following
                GPIO.output(BLUE_LED, False)
                GPIO.output(RED_LED, True)
                time.sleep(2)
                GPIO.output(RED_LED, False)
                GPIO.output(BLUE_LED, True)
                print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at area @ ",thetime
                cur.execute("INSERT INTO rejected (rejectedcard, whenrejected) VALUES(?,?)", (rfid_data, thetime))
                con.commit()                # logging unauthorised card into database
                cur.close()                 # closing DB connection
                continue
            else:                           # if card found execute the following
                GPIO.output(BLUE_LED, False)
                GPIO.output(GREEN_LED, True)
                time.sleep(2)
                GPIO.output(GREEN_LED, False)
                GPIO.output(BLUE_LED, True)
                print "Card found in DB."
                print result[0],"entered area @",thetime
                cur.execute("INSERT INTO tracking (card, name, lastentry) VALUES(?,?,?)",    (rfid_data, result[0], thetime))
                cur.execute("UPDATE RFID SET lastentry=(?) WHERE card=(?)",    (thetime, rfid_data))
                con.commit()               # log last entry into DB and log each scan into DB for tracking
                cur.close()
except KeyboardInterrupt:
    print "Caught interrupt, exiting..."
    print "Unexpected error:", sys.exc_info()[0]
    raise
finally:
    GPIO.cleanup()                         # cleanup GPIO
