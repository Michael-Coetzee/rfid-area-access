from evdev.device import InputDevice
from evdev.util import categorize
from evdev import ecodes
import evdev
import time, sys
import sqlite3 as lite
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

dev = InputDevice('/dev/input/event3')

keys = {
    2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9, 11: 0,
}

GREEN_LED = 18
BLUE_LED = 24
RED_LED = 23
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
# link to database
con = lite.connect('areaDatabase.db')
# connect to DB
cur = con.cursor()              

#create tables if they do not exist
cur.execute('CREATE TABLE IF NOT EXISTS employee (ID INTEGER PRIMARY KEY, Card TEXT, Name TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS tracking (ID INTEGER PRIMARY KEY, Card TEXT, Date DATETIME, Status INTEGER DEFAULT 0)')
cur.execute('CREATE TABLE IF NOT EXISTS rejected (ID INTEGER PRIMARY KEY, Card TEXT, Date TEXT)')
#example code: remove when in real world application just for testing purposes
cur.execute('REPLACE INTO employee values(0001, "2121743110", "Deon Spengler")')
cur.execute('REPLACE INTO employee values(0002, "2121723560", "Martin Heneck")')
cur.execute('REPLACE INTO employee values(0003, "2121741279", "Francois Kotze")')

GPIO.output(BLUE_LED, True)
code = []
rfid_data = ""
try:
    while True:
        # loop until tag is read
        thetime = time.strftime("%Y-%m-%d %a %H:%M:%S", time.localtime())
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == 00:
                    if event.code != 96:
                        try:
                            code.append(keys[event.code])
                            if len(code) >= 10:
                                rfid_data = "".join(map(str, code))
                                print "Card Scanned. Tag ID:", rfid_data  
                                cur.execute("SELECT Card, Name FROM employee WHERE Card = ?", [rfid_data])
                                # fetch name of card holder if exists
                                employee = cur.fetchone()
                                # if card not found execute the following code
                                if not employee:                
                                    GPIO.output(BLUE_LED, False)
                                    GPIO.output(RED_LED, True)
                                    time.sleep(2)
                                    GPIO.output(RED_LED, False)
                                    GPIO.output(BLUE_LED, True)
                                    print "UNAUTHORIZED CARD! [",rfid_data,"] scanned at area @ ",thetime
                                    # logging unauthorised card into database
                                    cur.execute("INSERT INTO rejected (Card, Date) VALUES(?,?)", (rfid_data, thetime))
                                    con.commit()                
                                    continue
                                    # if card found execute the following
                                else:
                                    GPIO.output(BLUE_LED, False)
                                    GPIO.output(GREEN_LED, True)
                                    time.sleep(2)
                                    GPIO.output(GREEN_LED, False)
                                    GPIO.output(BLUE_LED, True)
                                    print "Card found in DB."

                                    # get last record for card
                                    cur.execute("SELECT Status FROM tracking WHERE Card = ? ORDER BY datetime(Date) DESC LIMIT 1", [employee[0]])
                                    employeeStatus = cur.fetchone()

                                    if not employeeStatus or employeeStatus[0] == 0:
                                        cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, time.time(), 1))
                                        print employee[1],"entered area @", thetime
                                    elif employeeStatus[0] == 1:
                                        cur.execute("INSERT INTO tracking (Card, Date, Status) VALUES(?,?,?)", (rfid_data, time.time(), 0))
                                        print employee[1],"left area @", thetime
                                        # commit changes to database 
                                        con.commit()
                        except:
                            code = []
                            rfid_data = ""

except KeyboardInterrupt:
    print "Caught interrupt, exiting..."
    print "Unexpected error:", sys.exc_info()[0]
    raise
finally:
    # close connection
    cur.close()
     # cleanup GPIO
    GPIO.cleanup()                        
